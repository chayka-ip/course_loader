// ==UserScript==
// @name         pars
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        https://somesite.com/*
// @icon         https://www.google.com/s2/favicons?domain=tampermonkey.net
// @grant        none
// ==/UserScript==

// This script parses download links from lecture page

(function() {
    'use strict';

    let resultObj ={}

    const heading = document.getElementById("lecture_heading");

    resultObj.title = heading.textContent.trim()
    resultObj.url = heading.getAttribute("data-lecture-url")

    const dlElements = document.getElementsByClassName("download");

    let dlLinks = []

    for(const elem of dlElements){
        const dlRef = elem.href
        dlLinks.push(dlRef)
    }

    resultObj.download_links = dlLinks

    const parts = resultObj.url.split("/") // 2,4 get
    const fileName = parts[2] + "-" + parts[4] + "-" + resultObj.title + ".json" // course - lecture - lecture title
    const resultText = JSON.stringify(resultObj)

    const foundDownloads = resultObj.download_links.length > 0
    if(foundDownloads) download(fileName, resultText)

})();

function download(filename, text) {
  var element = document.createElement('a');
  element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
  element.setAttribute('download', filename);

  element.style.display = 'none';
  document.body.appendChild(element);

  element.click();

  document.body.removeChild(element);
}


