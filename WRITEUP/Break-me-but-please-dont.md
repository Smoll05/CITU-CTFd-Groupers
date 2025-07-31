## Challenge Name: Break me but please don't
Category: Web Exploitation  
Points: 150   

### Challenge Description:  
We were presented with a minimal webpage showing only an image and a line of text that says **"please don't break me"**. It appeared harmless, but something seemed off.

---

### Approach

**1. Viewing the page source revealed a hidden script with a flag array**

```html
<script>
    const flagArray = [43,49,54,55,"7b",65,61,73,79,"5f","6c",61,"6d",61,"6e",67,"5f",76,69,65,77,73,"6f",75,72,63,65,"7d"];
    const flag = flagArray.map(charCode => String.fromCharCode(charCode)).join('');
    const urlParams = new URLSearchParams(window.location.search);
    const name = urlParams.get('name');
    if (name === 'CITU') {
        alert(flag);
    } else {
        throw new Error(flag);
    }
</script>
```

We saw that a flag was constructed using an array of decimal and hexadecimal values and shown only when the URL parameter `name` is set to `CITU`.

So we tried appending:

```
/?name=CITU
```

to the URL.

![alert prompt](https://raw.githubusercontent.com/Smoll05/CITU-CTFd-Groupers/main/Writeup-Images/pop-weasel-prompt.png)


**2. The output was garbled due to mixed character code formats**

Although we got an alert popup, the flag appeared garbled. This was likely because `String.fromCharCode()` cannot correctly process hex strings (`"7b"`, `"6c"` etc.) directly mixed with decimal numbers.

We then copied the hex parts of the array and used a **Hex to ASCII converter** to decode them manually. This gave us the correct flag:

```
CITU{easy_lamang_viewsource}
```

[Home](../..)