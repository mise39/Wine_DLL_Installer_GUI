# 本程式是配合Protontricks使用的,方便Galgame修正遊戲影片/部份動態畫面的程式。
本程式建構於 5% Claude + 75% ChatGPT + 20% 人工修正，  
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
[1.0教學影片](https://www.youtube.com/watch?v=L_7x6o2Gjdk) 

[2.0示範影片](https://www.youtube.com/watch?v=sc6kIWUgoF4) 

3.0 增加英文版，Proton資料刪除鍵 


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

---
# English Version
# This program is designed to work with Protontricks, facilitating the correction of game videos and some dynamic scenes in Galgames.
This program is built with 5% Claude, 75% ChatGPT, and 20% manual corrections.  
It does not include network functionality and requires no additional Python plugins.

## Usage Instructions:
1. Download the .sh and .py files.  
2. Open the Konsole terminal.  
3. Enter the following command:

```
chmod +x /your/file/location/wine_dll_installer_gui.sh

```
4. Add this ".sh" file to non-Steam games, then execute it.

## Detailed Guide/Demo Videos:  
[Version 1.0 Tutorial Video](https://www.youtube.com/watch?v=L_7x6o2Gjdk)  
[Version 2.0 Demo Video](https://www.youtube.com/watch?v=sc6kIWUgoF4)  

Version 3.0 adds English support and a Proton data deletion key.

## *Solution for "Chmod not found" Error  
In the Konsole, first enter:
```
passwd

```
Set a password, then enter:  
```
sudo pacman -Sy coreutils
```
The chmod command should no longer report errors.
