    const flagArray = [67,73,84,85,123,99,111,111,107,105,101,95,112,97,115,116,97,125];
    const flag = flagArray.map(charCode => String.fromCharCode(charCode)).join('');
    document.cookie = `flag=${flag};`;