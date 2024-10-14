
## 必要なパッケージを Lambda Layerとして設定する

* Lambda Layer の作成

```
mkdir python

pip install requests==2.27.1 BeautifulSoup4==4.12.3 -t ./python

zip -r Layer.zip python/       
```

* 作成した Layer.zip を AWS Lambda Layer として設定 
