## Challenge Name: I love cookies 
Category: Web Exploitation  
Points: 150


### Challenge Description:  
The title and layout of the website features the Cookie Monster, giving us a big hint that cookies play an important role in this challenge.

---

### Approach

**1. Inspecting browser cookies revealed the flag**

By opening the browser's developer tools and navigating to the **Storage > Cookies** section, we were able to directly see the flag stored in a cookie:

![Cookie View](https://raw.githubusercontent.com/Smoll05/CITU-CTFd-Groupers/main/Writeup-Images/cookie-view.png)


```
flag=CITU{cookie_pasta}
```

This was a clear indication that the flag was intentionally hidden in the site's cookies.

**2. Viewing the page source and the external JavaScript file**

```js
const flagArray = [67,73,84,85,123,99,111,111,107,105,101,95,112,97,115,116,97,125];
const flag = flagArray.map(charCode => String.fromCharCode(charCode)).join('');
document.cookie = `flag=${flag};`;
```

This snippet from `script.js` confirmed how the flag got into the cookie. It converts character codes into the string `CITU{cookie_pasta}` and sets it as a browser cookie.
