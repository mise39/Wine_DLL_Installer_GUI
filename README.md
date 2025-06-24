# 本程式是配合Protontricks使用的,方便Galgame修正遊戲影片/部份動態畫面的程式。
本程式建構於20% Claude + 75% ChatGPT + 5% 人工修正，  
不帶網絡功能，無需任何Python額外插件。  

## 使用方法:
1. 先下載.sh和.py檔案  
2. 開啟Konsole指令台。  
3. 輸入指令
```
chmox +x /你的檔案位置/wine_dll_installer_gui.sh
```
4.把這個".sh"加入到非Steam遊戲，然後再執行。  

## 詳細/示範影片:  
https://www.youtube.com/watch?v=L_7x6o2Gjdk

## *關於Chmod not found的解決方法  
請先konsole輸入
```
passwd
```
設定密碼
然後再輸入  
```
sudo pacman -Sy coreutils
```
Chmod 指令就不會報錯  
