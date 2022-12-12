
/**
 * @fileoverview Template to compose HTTP reqeuest.
 * 
 */

const url = `https://api.nebula-emby.com/api/userCheckIn?data=query_id%3DAAF31fQyAAAAAHfV9DLNEPed%26user%3D%257B%2522id%2522%253A854906231%252C%2522first_name%2522%253A%2522%25E5%25AD%2590%2522%252C%2522last_name%2522%253A%2522%25E9%259D%259E%25E4%25BD%2599%2522%252C%2522username%2522%253A%2522shexiaoyu%2522%252C%2522language_code%2522%253A%2522zh-hans%2522%257D%26auth_date%3D1670829811%26hash%3D8fd00992dba3e7d2811ac86778d6851fbcde273542f18b414c52af0bcdb4d384`;
const method = `GET`;
const headers = {
'Accept-Encoding' : `gzip, deflate, br`,
'Accept' : `application/json, text/plain, */*`,
'Connection' : `keep-alive`,
'Referer' : `https://api.nebula-emby.com/web/index.html`,
'Host' : `api.nebula-emby.com`,
'User-Agent' : `Mozilla/5.0 (iPhone; CPU iPhone OS 15_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148`,
'Accept-Language' : `zh-CN,zh-Hans;q=0.9`
};
const body = ``;

const myRequest = {
    url: url,
    method: method,
    headers: headers,
    body: body
};

$task.fetch(myRequest).then(response => {
    console.log(response.statusCode + "\n\n" + response.body);
    $done();
}, reason => {
    console.log(reason.error);
    $done();
});
