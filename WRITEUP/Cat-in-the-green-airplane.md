## Challenge Name: Cat in the Green Airplane  
Category: MISC
Points: 150  

### Challenge Description:  
An image of a cat in a green airplane is given. No text or obvious clue is visible at first glance.

---

### Approach

**1. Inspecting the image using image analysis tools**

We attempted to adjust the RGB values manually in GIMP, which began to reveal artifacts. However, for faster results, we used [aperisolve.fr](http://aperisolve.fr), an online OSINT tool that automates steganographic and metadata analysis.

![Cat in green airplane](https://raw.githubusercontent.com/Smoll05/CITU-CTFd-Groupers/main/Writeup-Images/Cat-Green-Airplane.png)

This revealed a hidden frame embedded within the image which contained the flag:

```
CITU{hidden_frame101}
```