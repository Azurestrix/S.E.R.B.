Inventory management Kivy program which is quite finished (works both on pc and android) albeit however efforts to convert it into an apk failed so far, I did uploaded the buildozer file; it should work(it is) but I could not figure out even with catlog why it crashes on android.  
It connects to Google Sheets and writes/reads out information.  

Known bugs:    
-I did not handled errors at uploads where internet is not working so with no or bad internet connection it will error out quite ungracefully.

-In the ReceiveMenu when intaking multiple items after each other if you want the LOT or PRDUCTIONDATE value N/A it will be still the value of the previous one and thus need to restart the whole program so it empties the memory.

I included a quite simplified MS Visio "documentation" its not the most throughout but I tried to make the program quite easy to understand anyway (I did however left quite plenty of comments for myself in the code which I did not deleted and should be a good well reasonably good guide).

There would be / could be plenty of stuff to do on this project especially with DRY but maybe in the future, now I want to explore new projects this one is quite usable anyway and I do use it daily.

PS: You need a Google Sheets authentication .json for it and the document is in Microsoft Visio format.
