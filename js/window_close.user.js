// ==UserScript==
// @name         window close
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        https://somesite.com/courses/*
// @icon         data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
    const closeWait = 5000
    window.setTimeout(window.top.close, closeWait);

     //window.top.close();

})();