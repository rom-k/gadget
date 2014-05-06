#include<windows.h>
#include<winbase.h>

int WINAPI WinMain(
	HINSTANCE hInstance,
	HINSTANCE hPrevInstance,
	PSTR lpCmdLine,
	int nCmdShow) {

	HANDLE hFile;
	DWORD dwWriteSize;
	LPSTR lpFileName = "C:\\temp\\test.txt";
	LPSTR lpText     = "Debug Training";

	hFile = CreateFile(
		lpFileName, GENERIC_WRITE, 0, NULL,
		CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL
		);

	DebugBreak();

	WriteFile(hFile, lpText, lstrlen(lpText), &dwWriteSize, NULL);

	CloseHandle(hFile);

	return 0;
}