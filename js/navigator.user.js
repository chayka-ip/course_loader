// ==UserScript==
// @name         navigator
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        https://somesite.com/
// @icon         data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==
// @grant        none
// ==/UserScript==

// Site content is dynamically generated. This script opens browser pages with urls provided

(function() {
    'use strict';

    const domain = "https://somesite.com"
    const wait = 5000

    const run = !true

    if(!run) return;

    let numItem = 0

    const linkMap = getData()
    for(const courseLinks of linkMap){
        for(const lecture of courseLinks){
            numItem += 1
            let url = domain + lecture
            url = lecture

            const timeOut = numItem * wait
            window.setTimeout(()=> navigate(url), timeOut);
        }
    }


})();

function navigate(url){
   window.open(url, '_blank').focus();
}

function sleep(milliseconds) {
  const date = Date.now();
  let currentDate = null;
  do {
    currentDate = Date.now();
  } while (currentDate - date < milliseconds);
}

function getData(){

return [

    ['/courses/course1_name/lectures/lecture_1', ... '/courses/course1_name/lectures/lecture_9999'],
    ['/courses/course2_name/lectures/lecture_1', ... '/courses/course2_name/lectures/lecture_574'],
    ['/courses/course3_name/lectures/lecture_1', ... '/courses/course3_name/lectures/lecture_322']
]
}
