## vertification and development environment
tutorialsのファイルを入れて動くか試す。JSONでもよい。
> tutorialsのファイルは無事動いたが、pingができない。コンテナノードにiputil-pingをインストールしてもだめだった。containernet自体にpingを入れないとダメかもしれない。
### Python
使いたいJSONによってs1の部分を変える。
### Makefile
全部コンパイルしたいファイル名に変える。  
> tutorialsのファイルも適切にMakefileを更新すればmake出来た
## capsule.p4
### Parser

### Ingress
カスタムヘッダの追加
### Deparser
カスタムヘッダも追加で出力