Inventory management program which is quite albeit efforts to convert it into apk however failed so far, I did uploaded the buildozer file it should work but I could not figure out even with catlog why it crashes on android.  
It connects to google sheets and writes/reads out information.  

Known bugs:    
-I did not handled errors at uploads where internet is not working so with no/bad intternet connection it will error out quite ungracefully.

-In the ReceiveMenu when intaking multiple itemsafter each other if you want the LOT or PRDUCTIONDATE N/A it will be still the value of the previous one and thus need to restars the whole program so it empties the memory.

I included a quite simplified visio "documentation" its not the most throughout but I tried to make the program quite easy to understand (I did however left quite plenty of comments for myself in the code which I did not deleted).

There would be / could be plenty of stuff to do on this project escpeically with DRY but maybe in the future now I want to explore new projects this one is quite usable anyway and I do use it daily.

PS: You need a Google Sheets authentication .json for it and the document is in Microsoft Visio format.
