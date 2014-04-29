#include<windows.h>

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

	/*
	if (hFile == INVALID_HANDLE_VALUE) {
		MessageBox(
			NULL, TEXT("ファイルを作成できませんでした"),
			TEXT("エラー"), MB_OK
			);
		return 1;
	}
	*/

	WriteFile(hFile, lpText, lstrlen(lpText), &dwWriteSize, NULL);

	CloseHandle(hFile);

	return 0;
}