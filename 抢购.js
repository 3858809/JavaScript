
/**
 * @fileoverview Template to compose HTTP reqeuest.
 * 
 */

const url = `https://marathon.jd.com/seckillnew/orderService/submitOrder.action?skuId=2943430`;
const method = `POST`;
const headers = {
'Accept' : `application/json, text/plain, */*`,
'Origin' : `https://marathon.jd.com`,
'Accept-Encoding' : `gzip, deflate, br`,
'Cookie' : `__jd_ref_cls=MSecKillBalance_Order_Submit; mba_muid=16709832056661882836054.749.1671019658221; mba_sid=749.23; seckillSid=; seckillSku=2943430; __jda=123122771.16709832056661882836054.1670983205.1671013497.1671019205.3; __jdb=123122771.9.16709832056661882836054|3.1671019205; __jdc=123122771; __jdv=123122771%7Ckong%7Ct_1000170136%7Ctuiguang%7Cnotset%7C1670464822371; pre_seq=1; pre_session=ad47363cd85cdf31a34691156a9a4c8be2c0043a|1676; unpl=JF8EAMNnNSttXR5UUklRS0VATFwEW1VYHx8DbzQBAFQMHFcBTlBLGxJ7XlVdXhRLFB9uYRRUWlNIUQ4ZBCsiEEpcVV9UAEIfAV9nAVIzWSVUDB5sdREYTQ1dCw1cTBICaDACB15oe1cFKwMrEhdNXFFfXQ1NEgpvYwBXVV1DUwMYMhoiEENZZF5cCUkeAG5nBlNYWUpXNSsGHREWT1xVX144SicCXyZrUlxaTFwCVgIcFBFOXFRbWw1CFwdqZA1RVV9NVzUaMhg%7CJF8EAOJnNSttX0sGB04DHUURSVxSW18BT0cCbGAEVl5cTgQFT1JLFRR7XlVdXhRLFB9uZxRUVVNJXA4aBisSFHteVVxcDUITBm1gNVRVXkJVBxoCKxIVSTNWWlQIThQHamRrVF02e1cFKwMrQkVOW1ZZX1oeHgc9MlJWXQhJUQITAhsWFxtVBFsPARhDAD1mBFFfCHtVNRIDKxIRSlpXX1UJSRUKaWcGZG1Ze1U1GjJafBBKWl1dXAxMWlM6YgNWWloZAQwfUE5FEksNVltaAEsXB2g3DQRYCkIHURhQGhMVSQ1kX20I; pt_key=app_openAAJjmS2DADArk7ruINmj383OT845elIgog2dz7NLbcp8VGaMUATjjkO6ieqcog7KutcX7o-qSzs; pt_pin=jd_4c814a9fcafb5; pwdt_id=jd_4c814a9fcafb5; sid=b08f22c4327cece8e70031375b0e8acw; mid=bGzRPGqEYzIcpevPE-VunwRyFymvVBRp0iNByyIxxaw; qid_seq=2; qid_sid=724905af-50d6-4a8a-84df-5fb9b6ee46e7-2; qid_ls=1671013511276; qid_ts=1671018912510; qid_vis=2; UUID=6FD0073A-E341-4BD3-A26E-68714E161D74; deviceId=ad47363cd85cdf31a34691156a9a4c8be2c0043a; deviceType=iPhone9,4; jdpay_appId=com.360buy.jdmobile; jdpay_appVersion=168158; jdpay_browserId=pay; jdpay_sdkVersion=4.00.44.00; moduleBuildVersion=13; moduleName=JDPaySDK; moduleVersion=4.00.44.00; osPlatform=iOS; 3AB9D23F7A4B3C9B=TJVHMEYXNUZCN6FL3WFC3BP7ZNLHCFLPCPZHMSSDRYRFCHW54VYOX3CA4IWNMRL2KFMBC65TJ5YI47ZCLBMZYYQ3N4; _gia_s_e_joint={"eid":"TJVHMEYXNUZCN6FL3WFC3BP7ZNLHCFLPCPZHMSSDRYRFCHW54VYOX3CA4IWNMRL2KFMBC65TJ5YI47ZCLBMZYYQ3N4","ma":"","im":"","os":"iOS","osv":"","ip":"220.249.162.85","apid":"jdapp","ia":"","uu":"","cv":"11.1.2","nt":"UNKNOW","at":"1"}; __jdu=16709832056661882836054; _gia_s_local_fingerprint=997e69e8119ca39ebf071e8004e24c71; wxa_level=1; qid_fs=1671013511273; qid_uid=724905af-50d6-4a8a-84df-5fb9b6ee46e7; BATQW722QTLYVCRD={"tk":"jdd01MLCRRO45TRIBXF3F5HEQQFT2XJJS3KC6BNNGQGSDIKWW23KSTC76ZXNFFGWZDMBSBQE3QRPMSKWMIHROQOVSCQ4PVVMAY4ALC54IMMY01234567","t":1670985067982}`,
'Content-Type' : `application/x-www-form-urlencoded`,
'Host' : `marathon.jd.com`,
'Connection' : `keep-alive`,
'User-Agent' : `jdapp;iPhone;11.1.2;;;M/5.0;appBuild/168158;jdSupportDarkMode/0;ef/1;ep/%7B%22ciphertype%22%3A5%2C%22cipher%22%3A%7B%22ud%22%3A%22YWG0DzC2C2DuENVtZQYzCWOzDNY5CJO1DwO5YJHtEQTvCwCmCNGzYG%3D%3D%22%2C%22sv%22%3A%22CJUkDy4n%22%2C%22iad%22%3A%22%22%7D%2C%22ts%22%3A1671019333%2C%22hdid%22%3A%22JM9F1ywUPwflvMIpYPok0tt5k9kW4ArJEU3lfLhxBqw%3D%22%2C%22version%22%3A%221.0.3%22%2C%22appname%22%3A%22com.360buy.jdmobile%22%2C%22ridx%22%3A-1%7D;Mozilla/5.0 (iPhone; CPU iPhone OS 15_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148;supportJDSHWK/1;`,
'Referer' : `https://marathon.jd.com/seckillM/seckill.action?skuId=2943430&num=1&rid=1671019337`,
'Accept-Language' : `zh-CN,zh-Hans;q=0.9`
};
const body = `num=1&addressId=6658015552&name=%E4%BD%98%E5%B0%8F%E9%B1%BC&provinceId=16&provinceName=%E7%A6%8F%E5%BB%BA&cityId=1303&cityName=%E7%A6%8F%E5%B7%9E%E5%B8%82&countyId=48716&countyName=%E9%97%BD%E4%BE%AF%E5%8E%BF&townId=48765&townName=%E4%B8%8A%E8%A1%97%E9%95%87&addressDetail=%E9%A9%AC%E6%8E%92%E6%9D%91%E9%AB%98%E5%B2%90%E8%B7%AF%E5%9B%BD%E8%B4%B8%E4%B9%9D%E6%BA%AA%E5%8E%9F%202%E6%A0%8B1702%E5%8D%95%E5%85%83&mobile=156%2A%2A%2A%2A0117&mobileKey=397b04dffbaa54126664e47c15b382b6&invoiceTitle=4&invoiceContent=1&invoicePhone=156%2A%2A%2A%2A0117&invoicePhoneKey=397b04dffbaa54126664e47c15b382b6&invoice=true&password=&codTimeType=3&paymentType=4&overseas=0&phone=&areaCode=86&token=f874ca3a3f1479c3c50e8e97238a0870&sk=ULO51LHCJCUFOZTTAUDNUHYV&skuId=2943430`;

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
