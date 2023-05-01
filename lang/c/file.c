// インクルードファイル
#include <stdio.h>
#include <stdbool.h>
#include <stdint.h>
#ifdef _WIN32
 #include <direct.h>
#else
 #include <sys/stat.h>
#endif

// 各種定義 
#ifdef _WIN32
 #define MKDIR(name) mkdir(name)
#else
 #define MKDIR(name) mkdir(name, S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH)
#endif

// ダンプのディレクトリとファイル名の定義
#define DUMP_DIR_NAME           ("DUMP")
#define DUMP_FILE_NAME          ("audio")
#define DUMP_FILE_NAME_SIZE     (50)

// プロトタイプ宣言
bool open_file(char *, FILE **);
bool close_file(FILE **);
bool write_file(uint8_t *, uint32_t, uint32_t, FILE **);
bool check_exist_file(char *);

bool open_file(char *base_name, FILE **fp)
{
    char file_name[50];

    for (int i = 0; i < 1000; i++)
    {
        sprintf(file_name, "%s_%03d.bin", base_name, i);
        if (!check_exist_file(file_name))
        {
            *fp = fopen(file_name, "ab");
            if (*fp != NULL)
            {
                // success create file
                return true;
            }
            else
            {
                // fail create file
                printf("create file: fail(%s)\n", file_name);
                return false;
            }
        }
    }
    //  exist base_name file over 1000 
    return false;
}

bool close_file(FILE **fp)
{
    int ret = fclose(*fp);

    if (ret != 0)
    {
        printf("close file: fail\n");
        return false;
    }

    return true;
}

bool write_file(uint8_t* data, uint32_t unit, uint32_t size, FILE **fp)
{
    size_t written = fwrite(data,unit, size, *fp);

    if (written != size)
    {
        printf("write file: fail\n");
        return false;
    }

    return true;
}

bool check_exist_file(char *file_name)
{
    FILE *fp;
    fp = fopen(file_name, "r");
    if (fp != NULL)
    {
        // exist 
        return true;
    }
    else
    {
        // no exist
        return false;
    }
    fclose(fp);
}

int main(void)
{
    FILE *fp;
    bool ret;

    MKDIR(DUMP_DIR_NAME);
    char base_name[DUMP_FILE_NAME_SIZE]; // ファイルサイズは動的に決めるべき
    sprintf(base_name, "%s/%s", DUMP_DIR_NAME, DUMP_FILE_NAME);

    ret = open_file(base_name, &fp);


    // wite処理を入れる

    if (ret)
    {
        printf("success create\n");

        ret = close_file(&fp);
    }
    else
    {
        printf("fail create\n");
    }
    return 0;
}
