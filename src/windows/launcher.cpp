// SPDX-License-Identifier: MPL-2.0
// Development launcher for a separately built, private Writer runtime.
#define UNICODE
#define _UNICODE
#include <windows.h>
#include <shellapi.h>
#include <string>
#include <filesystem>
#include <vector>
#include <cwctype>

static std::wstring quote(const std::wstring& s) {
    std::wstring result=L"\"";
    size_t slashes=0;
    for(wchar_t c:s) {
        if(c==L'\\') { ++slashes; continue; }
        if(c==L'"') { result.append(slashes*2+1,L'\\'); result+=c; }
        else { result.append(slashes,L'\\'); result+=c; }
        slashes=0;
    }
    result.append(slashes*2,L'\\'); result+=L'"'; return result;
}
static int fail(const wchar_t* msg) {
    MessageBoxW(nullptr,msg,L"ViPrima Writer — Development Build",MB_OK|MB_ICONERROR);
    return 1;
}
int WINAPI wWinMain(HINSTANCE,HINSTANCE,PWSTR,int) {
    namespace fs=std::filesystem;
    std::vector<wchar_t> buf(32768);
    DWORD n=GetModuleFileNameW(nullptr,buf.data(),static_cast<DWORD>(buf.size()));
    if(!n || n>=buf.size()) return fail(L"Cannot resolve installation directory.");
    fs::path root=fs::path(std::wstring(buf.data(),n)).parent_path();
    fs::path engine=root/L"runtime"/L"program"/L"soffice.exe";
    std::error_code ec;
    if(!fs::is_regular_file(engine,ec)) return fail(L"The private Writer runtime is missing. Reinstall the development package.");
    int argc=0; LPWSTR* argv=CommandLineToArgvW(GetCommandLineW(),&argc);
    if(!argv) return fail(L"Cannot read command line.");
    // bootstrap uses a profile relative to the user's home, separate from upstream Office.
    std::wstring cmd=quote(engine.wstring())+L" -env:UserInstallation=$SYSUSERCONFIG/ViPrima/WriterDev --writer --nofirststartwizard";
    for(int i=1;i<argc;++i) {
        fs::path file(argv[i]);
        // Reject UNC/device paths and mapped network drives before touching the file.
        const auto raw=file.wstring();
        if(raw.size()<3 || !((raw[0]>=L'A' && raw[0]<=L'Z') || (raw[0]>=L'a' && raw[0]<=L'z')) || raw[1]!=L':' || (raw[2]!=L'\\' && raw[2]!=L'/') || GetDriveTypeW(file.root_path().c_str())!=DRIVE_FIXED) {
            LocalFree(argv); return fail(L"Open a document stored on a local fixed drive.");
        }
        if(!file.is_absolute() || !fs::is_regular_file(file,ec)) { LocalFree(argv); return fail(L"Only existing absolute local document paths are accepted."); }
        auto ext=file.extension().wstring();
        for(auto& c:ext) c=static_cast<wchar_t>(towlower(c));
        if(ext!=L".docx" && ext!=L".odt" && ext!=L".rtf" && ext!=L".txt") {LocalFree(argv);return fail(L"Unsupported document type for this development launcher.");}
        cmd+=L" "+quote(file.wstring());
    }
    LocalFree(argv);
    STARTUPINFOW si{}; si.cb=sizeof(si); PROCESS_INFORMATION pi{};
    if(!CreateProcessW(engine.c_str(),cmd.data(),nullptr,nullptr,FALSE,0,nullptr,engine.parent_path().c_str(),&si,&pi)) return fail(L"Unable to start the private Writer runtime.");
    CloseHandle(pi.hThread);CloseHandle(pi.hProcess);return 0;
}
