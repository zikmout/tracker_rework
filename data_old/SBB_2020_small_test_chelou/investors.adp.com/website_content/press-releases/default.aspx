<!DOCTYPE HTML>
<html xmlns="http://www.w3.org/1999/xhtml" lang="en-US" xml:lang="en-US">
<head><title>
	Automatic Data Processing - Press Releases
</title><meta content="text/html; charset=UTF-8" http-equiv="Content-type" /><meta content="RevealTrans(Duration=0,Transition=0)" http-equiv="Page-Enter" /><meta content="IE=edge,chrome=1" http-equiv="X-UA-Compatible" /><script type="text/javascript">window.NREUM||(NREUM={});NREUM.info = {"beacon":"bam.nr-data.net","errorBeacon":"bam.nr-data.net","licenseKey":"4b6f7f959c","applicationID":"229922501","transactionName":"b1xWMUIDWBdWARFYX1YWdTZgTVIBUQMQXUQWWEcVSA==","queueTime":0,"applicationTime":547,"agent":"","atts":""}</script><script type="text/javascript">(window.NREUM||(NREUM={})).loader_config={licenseKey:"4b6f7f959c",applicationID:"229922501"};window.NREUM||(NREUM={}),__nr_require=function(e,n,t){function r(t){if(!n[t]){var i=n[t]={exports:{}};e[t][0].call(i.exports,function(n){var i=e[t][1][n];return r(i||n)},i,i.exports)}return n[t].exports}if("function"==typeof __nr_require)return __nr_require;for(var i=0;i<t.length;i++)r(t[i]);return r}({1:[function(e,n,t){function r(){}function i(e,n,t){return function(){return o(e,[u.now()].concat(f(arguments)),n?null:this,t),n?void 0:this}}var o=e("handle"),a=e(4),f=e(5),c=e("ee").get("tracer"),u=e("loader"),s=NREUM;"undefined"==typeof window.newrelic&&(newrelic=s);var p=["setPageViewName","setCustomAttribute","setErrorHandler","finished","addToTrace","inlineHit","addRelease"],l="api-",d=l+"ixn-";a(p,function(e,n){s[n]=i(l+n,!0,"api")}),s.addPageAction=i(l+"addPageAction",!0),s.setCurrentRouteName=i(l+"routeName",!0),n.exports=newrelic,s.interaction=function(){return(new r).get()};var m=r.prototype={createTracer:function(e,n){var t={},r=this,i="function"==typeof n;return o(d+"tracer",[u.now(),e,t],r),function(){if(c.emit((i?"":"no-")+"fn-start",[u.now(),r,i],t),i)try{return n.apply(this,arguments)}catch(e){throw c.emit("fn-err",[arguments,this,e],t),e}finally{c.emit("fn-end",[u.now()],t)}}}};a("actionText,setName,setAttribute,save,ignore,onEnd,getContext,end,get".split(","),function(e,n){m[n]=i(d+n)}),newrelic.noticeError=function(e,n){"string"==typeof e&&(e=new Error(e)),o("err",[e,u.now(),!1,n])}},{}],2:[function(e,n,t){function r(e,n){var t=e.getEntries();t.forEach(function(e){"first-paint"===e.name?c("timing",["fp",Math.floor(e.startTime)]):"first-contentful-paint"===e.name&&c("timing",["fcp",Math.floor(e.startTime)])})}function i(e,n){var t=e.getEntries();t.length>0&&c("lcp",[t[t.length-1]])}function o(e){if(e instanceof s&&!l){var n,t=Math.round(e.timeStamp);n=t>1e12?Date.now()-t:u.now()-t,l=!0,c("timing",["fi",t,{type:e.type,fid:n}])}}if(!("init"in NREUM&&"page_view_timing"in NREUM.init&&"enabled"in NREUM.init.page_view_timing&&NREUM.init.page_view_timing.enabled===!1)){var a,f,c=e("handle"),u=e("loader"),s=NREUM.o.EV;if("PerformanceObserver"in window&&"function"==typeof window.PerformanceObserver){a=new PerformanceObserver(r),f=new PerformanceObserver(i);try{a.observe({entryTypes:["paint"]}),f.observe({entryTypes:["largest-contentful-paint"]})}catch(p){}}if("addEventListener"in document){var l=!1,d=["click","keydown","mousedown","pointerdown","touchstart"];d.forEach(function(e){document.addEventListener(e,o,!1)})}}},{}],3:[function(e,n,t){function r(e,n){if(!i)return!1;if(e!==i)return!1;if(!n)return!0;if(!o)return!1;for(var t=o.split("."),r=n.split("."),a=0;a<r.length;a++)if(r[a]!==t[a])return!1;return!0}var i=null,o=null,a=/Version\/(\S+)\s+Safari/;if(navigator.userAgent){var f=navigator.userAgent,c=f.match(a);c&&f.indexOf("Chrome")===-1&&f.indexOf("Chromium")===-1&&(i="Safari",o=c[1])}n.exports={agent:i,version:o,match:r}},{}],4:[function(e,n,t){function r(e,n){var t=[],r="",o=0;for(r in e)i.call(e,r)&&(t[o]=n(r,e[r]),o+=1);return t}var i=Object.prototype.hasOwnProperty;n.exports=r},{}],5:[function(e,n,t){function r(e,n,t){n||(n=0),"undefined"==typeof t&&(t=e?e.length:0);for(var r=-1,i=t-n||0,o=Array(i<0?0:i);++r<i;)o[r]=e[n+r];return o}n.exports=r},{}],6:[function(e,n,t){n.exports={exists:"undefined"!=typeof window.performance&&window.performance.timing&&"undefined"!=typeof window.performance.timing.navigationStart}},{}],ee:[function(e,n,t){function r(){}function i(e){function n(e){return e&&e instanceof r?e:e?c(e,f,o):o()}function t(t,r,i,o){if(!l.aborted||o){e&&e(t,r,i);for(var a=n(i),f=v(t),c=f.length,u=0;u<c;u++)f[u].apply(a,r);var p=s[y[t]];return p&&p.push([b,t,r,a]),a}}function d(e,n){h[e]=v(e).concat(n)}function m(e,n){var t=h[e];if(t)for(var r=0;r<t.length;r++)t[r]===n&&t.splice(r,1)}function v(e){return h[e]||[]}function g(e){return p[e]=p[e]||i(t)}function w(e,n){u(e,function(e,t){n=n||"feature",y[t]=n,n in s||(s[n]=[])})}var h={},y={},b={on:d,addEventListener:d,removeEventListener:m,emit:t,get:g,listeners:v,context:n,buffer:w,abort:a,aborted:!1};return b}function o(){return new r}function a(){(s.api||s.feature)&&(l.aborted=!0,s=l.backlog={})}var f="nr@context",c=e("gos"),u=e(4),s={},p={},l=n.exports=i();l.backlog=s},{}],gos:[function(e,n,t){function r(e,n,t){if(i.call(e,n))return e[n];var r=t();if(Object.defineProperty&&Object.keys)try{return Object.defineProperty(e,n,{value:r,writable:!0,enumerable:!1}),r}catch(o){}return e[n]=r,r}var i=Object.prototype.hasOwnProperty;n.exports=r},{}],handle:[function(e,n,t){function r(e,n,t,r){i.buffer([e],r),i.emit(e,n,t)}var i=e("ee").get("handle");n.exports=r,r.ee=i},{}],id:[function(e,n,t){function r(e){var n=typeof e;return!e||"object"!==n&&"function"!==n?-1:e===window?0:a(e,o,function(){return i++})}var i=1,o="nr@id",a=e("gos");n.exports=r},{}],loader:[function(e,n,t){function r(){if(!x++){var e=E.info=NREUM.info,n=d.getElementsByTagName("script")[0];if(setTimeout(s.abort,3e4),!(e&&e.licenseKey&&e.applicationID&&n))return s.abort();u(y,function(n,t){e[n]||(e[n]=t)}),c("mark",["onload",a()+E.offset],null,"api");var t=d.createElement("script");t.src="https://"+e.agent,n.parentNode.insertBefore(t,n)}}function i(){"complete"===d.readyState&&o()}function o(){c("mark",["domContent",a()+E.offset],null,"api")}function a(){return O.exists&&performance.now?Math.round(performance.now()):(f=Math.max((new Date).getTime(),f))-E.offset}var f=(new Date).getTime(),c=e("handle"),u=e(4),s=e("ee"),p=e(3),l=window,d=l.document,m="addEventListener",v="attachEvent",g=l.XMLHttpRequest,w=g&&g.prototype;NREUM.o={ST:setTimeout,SI:l.setImmediate,CT:clearTimeout,XHR:g,REQ:l.Request,EV:l.Event,PR:l.Promise,MO:l.MutationObserver};var h=""+location,y={beacon:"bam.nr-data.net",errorBeacon:"bam.nr-data.net",agent:"js-agent.newrelic.com/nr-1167.min.js"},b=g&&w&&w[m]&&!/CriOS/.test(navigator.userAgent),E=n.exports={offset:f,now:a,origin:h,features:{},xhrWrappable:b,userAgent:p};e(1),e(2),d[m]?(d[m]("DOMContentLoaded",o,!1),l[m]("load",r,!1)):(d[v]("onreadystatechange",i),l[v]("onload",r)),c("mark",["firstbyte",f],null,"api");var x=0,O=e(6)},{}],"wrap-function":[function(e,n,t){function r(e){return!(e&&e instanceof Function&&e.apply&&!e[a])}var i=e("ee"),o=e(5),a="nr@original",f=Object.prototype.hasOwnProperty,c=!1;n.exports=function(e,n){function t(e,n,t,i){function nrWrapper(){var r,a,f,c;try{a=this,r=o(arguments),f="function"==typeof t?t(r,a):t||{}}catch(u){l([u,"",[r,a,i],f])}s(n+"start",[r,a,i],f);try{return c=e.apply(a,r)}catch(p){throw s(n+"err",[r,a,p],f),p}finally{s(n+"end",[r,a,c],f)}}return r(e)?e:(n||(n=""),nrWrapper[a]=e,p(e,nrWrapper),nrWrapper)}function u(e,n,i,o){i||(i="");var a,f,c,u="-"===i.charAt(0);for(c=0;c<n.length;c++)f=n[c],a=e[f],r(a)||(e[f]=t(a,u?f+i:i,o,f))}function s(t,r,i){if(!c||n){var o=c;c=!0;try{e.emit(t,r,i,n)}catch(a){l([a,t,r,i])}c=o}}function p(e,n){if(Object.defineProperty&&Object.keys)try{var t=Object.keys(e);return t.forEach(function(t){Object.defineProperty(n,t,{get:function(){return e[t]},set:function(n){return e[t]=n,n}})}),n}catch(r){l([r])}for(var i in e)f.call(e,i)&&(n[i]=e[i]);return n}function l(n){try{e.emit("internal-error",n)}catch(t){}}return e||(e=i),t.inPlace=u,t.flag=a,t}},{}]},{},["loader"]);</script><meta content="width=device-width, initial-scale=1" name="viewport" /><meta content="3T9yKoza8iQsJyPN2EHx0FncSh0wmXQ3PSmhHJpWN6A" name="google-site-verification" /><script type='text/javascript'>window.mobileRedirect = { mobileEnabled: 0, deepLinkUrl: '/m/#deepLink/%7b%22view%22%3a%22PressReleaseList%22%2c%22languageId%22%3a%221%22%7d'}</script>
    <script type="text/javascript" src="/js/mobileRedirect.js">
    </script>
    
    <!--[if lte IE 8]>
<link id="respond-proxy" rel="respond-proxy" media="screen" href="//s23.q4cdn.com/483669984/files/js/respond-proxy.html" />
<link id="respond-redirect" rel="respond-redirect" media="screen" href="https://investors.adp.com/js/respond.proxy.gif" />
<![endif]-->

<link type="text/css" rel="stylesheet" media="all" href="//fonts.googleapis.com/css?family=Open+Sans:400,300,600" />
<link type="image/x-icon" rel="icon" media="" href="//s23.q4cdn.com/483669984/files/favicon.ico" />
<link type="image/x-icon" rel="shortcut icon" media="" href="//s23.q4cdn.com/483669984/files/favicon.ico" />
<link rel="stylesheet" media="print" href="//s23.q4cdn.com/483669984/files/css/print.css" />
<link id="htmlGlobalLinkCss" type="text/css" rel="stylesheet" media="all" href="//s23.q4cdn.com/483669984/files/css/global.css?v=32540" /><link id="htmlClientLinkCss" type="text/css" rel="stylesheet" media="all" href="//s23.q4cdn.com/483669984/files/css/client.css?v=32541" /><link id="htmlLinkPrintCss" type="text/css" rel="stylesheet" media="print" href="//s23.q4cdn.com/483669984/files/css/print.css" /><script type="text/javascript" src="//s23.q4cdn.com/483669984/files/js/q4.core.1.0.5.min.js"></script>
<script type="text/javascript" src="//s23.q4cdn.com/483669984/files/js/q4.app.1.0.5.min.js"></script>
<script type="text/javascript" src="https://widgets.q4app.com/widgets/q4.api.1.13.1.min.js"></script>
<script type="text/javascript" src="//s23.q4cdn.com/483669984/files/js/select2.min.js"></script>
<!--[if lte IE 8]>
<script type="text/javascript" src="https://investors.adp.com/js/respond.proxy.js"></script>
<![endif]-->

<script type="text/javascript">(function (i, s, o, g, r, a, m) {
    i['GoogleAnalyticsObject'] = r; i[r] = i[r] || function () {
        (i[r].q = i[r].q || []).push(arguments)
    }, i[r].l = 1 * new Date(); a = s.createElement(o),
        m = s.getElementsByTagName(o)[0]; a.async = 1; a.src = g; m.parentNode.insertBefore(a, m)
})(window, document, 'script', '//www.google-analytics.com/analytics.js', 'ga');

(function ($) {
    function initGaTracking(isp, org) {
        $.each(trackingCodes, function (i, data) {
            if (data.qualifier === "Q4") {
                ga('create', data.trackingCode, 'auto'); // Q4 tracker
                if (!!isp) ga('set', { 'dimension1': isp });
                if (!!org) ga('set', { 'dimension2': org });
                ga('set', 'anonymizeIp', true);
                ga('send', 'pageview', { 'page': location.pathname + location.search + location.hash }); // send pageview to Q4 tracker
            } else {
                ga('create', data.trackingCode, 'auto', { 'name': data.qualifier }); // Client tracker
                ga(data.qualifier + '.set', 'anonymizeIp', true);
                ga(data.qualifier + '.send', 'pageview', { 'page': location.pathname + location.search + location.hash }); // send pageview to Client tracker
            }
        });
    }

    var trackingCodes = [{qualifier: 'Client', trackingCode: 'UA-11111111-1'}];
    var ipSessStorageKey = 'ipApiInfo';
    var ipJsonStringified = sessionStorage.getItem(ipSessStorageKey);

    if (ipJsonStringified) {
        try {
            var ipJsonParsed = JSON.parse(ipJsonStringified);
            initGaTracking(ipJsonParsed.isp, ipJsonParsed.org);
        } catch (e) {
            console.error('Failed to JSON parse IP API session storage data\n', e);
            initGaTracking();
        }
    } else {
        $.getJSON('https://pro.ip-api.com/json/?key=xdjZbj0ZiVVozCo&fields=isp,org')
            .done(function (ipJson) {
                sessionStorage.setItem(ipSessStorageKey, JSON.stringify(ipJson));
                initGaTracking(ipJson.isp, ipJson.org);
            })
            .fail(function () {
                initGaTracking();
            });
    }
})(jQuery);
</script></head>
<body style="margin: 0px" class="BodyBackground">
    <input type="hidden" id="__RequestVerificationToken"/>
    
    
    <div id="pageClass" class="Sectionoverview PageDefault PagePressReleases LayoutOneColumnLayout Languageen-US">
        <div class="PageDefaultInner">
            <div id="litPageDiv" class="PagePressReleases SectionPressReleases ParentSection_overview">
                <a name="top"></a>
                <form action="default.aspx" method="post" id="fmForm1">
<div class="aspNetHidden">
<input type="hidden" name="__EVENTTARGET" id="__EVENTTARGET" value="" />
<input type="hidden" name="__EVENTARGUMENT" id="__EVENTARGUMENT" value="" />
<input type="hidden" name="__VIEWSTATE" id="__VIEWSTATE" value="" />
</div>

<script type="text/javascript">
//<![CDATA[
var theForm = document.forms['fmForm1'];
if (!theForm) {
    theForm = document.fmForm1;
}
function __doPostBack(eventTarget, eventArgument) {
    if (!theForm.onsubmit || (theForm.onsubmit() != false)) {
        theForm.__EVENTTARGET.value = eventTarget;
        theForm.__EVENTARGUMENT.value = eventArgument;
        theForm.submit();
    }
}
//]]>
</script>


<script src="/WebResource.axd?d=pynGkmcFUV13He1Qd6_TZDSH1oVlXKNmZSXd3zYZ2Gq6ERm6jivSb4ijerOGYkuGRtePZg2&amp;t=637100590445053551" type="text/javascript"></script>


<script type="text/javascript">
//<![CDATA[
function GetViewType(){ return '2'; }
function GetRevisionNumber(){ return '1'; }
function GetLanguageId(){ return '1'; }
function GetVersionNumber(){ return '5.31.1.1'; }
function GetViewDate(){{ return ''; }}
function GetSignature(){{ return ''; }}
//]]>
</script>

<script src="/WebResource.axd?d=x2nkrMJGXkMELz33nwnakMh5buNcZ-t3T4nCU0ZQt96Kk4JDhdv7pdb3Agzis1zDln1EUlimtVH-8O9nKu6Z_e6vBso1&amp;t=637100590445053551" type="text/javascript"></script>
<script type="text/javascript">
//<![CDATA[
function WebForm_OnSubmit() {
if (typeof(ValidatorOnSubmit) == "function" && ValidatorOnSubmit() == false) return false;
return true;
}
//]]>
</script>

                    
                    <a id="lnkPostback" href="javascript:__doPostBack(&#39;lnkPostback&#39;,&#39;&#39;)" style="display: none"></a>
                    
<div class="layout layout--one-column">
    <div class="layout_inner">
        <div class="layout_header">
            <div class="pane pane--header grid--no-gutter">
                <div class="pane_inner"><span class='HeaderPaneDiv'><span class='HeaderPaneDiv1'><div id="_ctrl0_ctl06_divModuleContainer" class="module module-embed module-skip">
    <div class="module_container module_container--outer">
        
        <div class="module_container module_container--inner">
            <a class="module-skip_link" href="#maincontent">Skip to main content</a>
        </div>
    </div>
</div></span><span class='HeaderPaneDiv2'><div id="_ctrl0_ctl09_divModuleContainer" class="module module-embed">
    <div class="module_container module_container--outer">
        
        <div class="module_container module_container--inner">
            <script type="text/javascript">
var Q4ApiKey = 'BF185719B0464B3CB809D23926182246';
</script>
        </div>
    </div>
</div></span><span class='HeaderPaneDiv3'><div id="_ctrl0_ctl12_divModuleContainer" class="module module-embed module-toggle module-toggle--mobile">
    <div class="module_container module_container--outer">
        
        <div class="module_container module_container--inner">
            <button type="button" class="module-toggle_button">
    <span class="module-toggle_button-top-line"></span>
    <span class="module-toggle_button-middle-line"></span>
    <span class="module-toggle_button-bottom-line"></span>
    <span class="sr-only"></span>
</button>
        </div>
    </div>
</div></span><span class='HeaderPaneDiv4'><div id="_ctrl0_ctl15_divModuleContainer" class="module module-embed module-header">
    <div class="module_container module_container--outer">
        
        <div class="module_container module_container--inner">
            <div class="module-header-items grid-flex">
    <div class="module-header-item-links">
        <div class="module-header-item module-header-item--logo">
            <a href="https://www.adp.com/"><img src="//s23.q4cdn.com/483669984/files/design/ADP-logo.svg" alt="Automatic Data Processing Logo"></a>
        </div>
        <div class="module-header-item module-header-item--corporate-links list--reset">
            <ul>
                <li><a href="https://www.adp.com/what-we-offer.aspx">What We Offer</a></li>
                <li><a href="https://www.adp.com/who-we-serve.aspx">Who We Serve</a></li>
                <li><a href="https://www.adp.com/resources.aspx">Resources</a></li>
                <li><a href="https://www.adp.com/about-adp.aspx">About ADP</a></li>
            </ul>
        </div>
    </div>
    <div class="module-header-item-buttons">
        <div class="module-header-item-buttons_desktop">
            <div class="module-header-item module-header-item--search-icon">
                <i class="q4-icon_search"></i>
            </div>
            <div class="module-header-item module-header-item--support-button">
                <a href="https://www.adp.com/contact-us/customer-service.aspx" class="button button--small button--inverted">Support</a>
                <div class="module-header-item_panel">
                    <div class="module-header-item_panel-container">
                        <div class="module-header-item_panel-row">
                            <a href="//www.adp.com/contact-us/support-for-employees.aspx"><span>I'm an employee of a company that uses ADP</span> Forms W2, 1099, etc., Payroll, Passwords and more.</a>
                        </div>
                        <div class="module-header-item_panel-row">
                            <a href="//www.adp.com/contact-us/support-for-client-administrators.aspx"><span>I'm an administrator that manages payroll, benefits or HR</span> Online access, questions, about paystubs, W2, 1099, and more.</a>
                        </div>
                        <div class="module-header-item_panel-row-link">
                            <a class="module_view-all-link" href="//www.adp.com/contact-us/customer-service.aspx"><span>More</span></a>
                        </div>
                    </div>
                </div>
            </div>
            <div class="module-header-item module-header-item--login-button">
                <a href="https://www.adp.com/logins.aspx" class="button button--red button--small">Login</a>
            </div>
        </div>
        <div class="module-header-item-buttons_mobile">
            <a href="https://www.adp.com/contact-us/customer-service.aspx">Contact</a>
            <a href="https://www.adp.com/logins.aspx">Login</a>
        </div>
    </div>
</div>
        </div>
    </div>
</div></span><span class='HeaderPaneDiv5'><div id="_ctrl0_ctl18_divModuleContainer" class="module module-html module-nav-text">
    <div class="module_container module_container--outer">
        
        <div class="module_container module_container--inner">
            <span class="module-nav_title-desktop"><a href="/">Investor Relations</a></span>
<div class="module-nav-ir_toggle">
    <a href="/">Investor Relations</a><button class="module-nav-ir_toggle-button q4-icon_chevron-down"><span class="sr-only"></span></button>
</div>
        </div>
    </div>
</div></span><span class='HeaderPaneDiv6'><nav class="nav nav--main "><ul class="level1">
	<li class="selected"><a href="https://investors.adp.com/press-releases/default.aspx">Press Releases</a></li><li><a href="https://investors.adp.com/events-and-presentations/default.aspx">Events & Presentations</a></li><li class="has-children"><a href="https://investors.adp.com/corporate-governance/board-of-directors/default.aspx">Corporate Governance</a><ul class="level2">
		<li><a href="https://www.adp.com/about-adp/leadership.aspx">Leadership Team</a></li><li><a href="https://investors.adp.com/corporate-governance/board-of-directors/default.aspx">Board of Directors</a></li><li><a href="https://investors.adp.com/corporate-governance/governance-documents/default.aspx">Governance Documents</a></li><li><a href="https://investors.adp.com/corporate-governance/committee-composition/default.aspx">Committee Composition</a></li><li><a href="https://www.adp.com/about-adp/corporate-social-responsibility/ethics.aspx">Code of Business Conduct and Ethics</a></li><li><a href="https://www.adp.com/about-adp/corporate-social-responsibility/ethics/code-of-ethics-for-principal-executive-officer-and-senior-financial-officers.aspx">Code of Ethics for Principal Executive Officer and Senior Financial Officer</a></li><li><a href="https://www.adp.com/about-adp/corporate-social-responsibility/ethics/anti-bribery-policy.aspx">Anti-Bribery Policy</a></li><li><a href="https://www.adp.com/about-adp/data-privacy.aspx">Data Privacy</a></li><li><a href="https://www.adp.com/about-adp/data-security.aspx">Data Security</a></li><li><a href="https://investors.adp.com/corporate-governance/contact-the-board/default.aspx">Contact the Board</a></li>
	</ul></li><li class="has-children"><a href="https://www.adp.com/about-adp/corporate-social-responsibility">CSR</a><ul class="level2">
		<li><a href="https://www.adp.com/about-adp/corporate-social-responsibility">CSR at ADP</a></li><li><a href="http://sustainability.adp.com/" target="_blank">Our CSR Report</a></li>
	</ul></li><li class="has-children"><a href="https://investors.adp.com/financial-information/sec-filings/default.aspx">Financial Information</a><ul class="level2">
		<li><a href="https://investors.adp.com/financial-information/sec-filings/default.aspx">SEC Filings</a></li><li><a href="https://investors.adp.com/financial-information/quarterly-results/default.aspx">Quarterly Results</a></li><li><a href="https://investors.adp.com/financial-information/annual-reports-and-proxies/default.aspx">Annual Reports & Proxies</a></li><li><a href="https://investors.adp.com/financial-information/letter-to-shareholders/default.aspx">Letter to Shareholders</a></li><li><a href="//s23.q4cdn.com/483669984/files/doc_financials/2020/q2/ADP-2Q20-Supplemental-Schedule.pdf" target="_blank">Supplemental Financial Data</a></li>
	</ul></li><li class="has-children"><a href="https://investors.adp.com/stock-information/stock-quote-and-chart/default.aspx">Stock Information</a><ul class="level2">
		<li><a href="https://investors.adp.com/stock-information/stock-quote-and-chart/default.aspx">Stock Quote & Chart</a></li><li><a href="https://investors.adp.com/stock-information/historical-price-lookup/default.aspx">Historical Price Lookup</a></li><li><a href="https://investors.adp.com/stock-information/investment-calculator/default.aspx">Investment Calculator</a></li><li><a href="https://investors.adp.com/stock-information/dividend-history/default.aspx">Dividend History</a></li><li><a href="https://investors.adp.com/stock-information/ownership-profile/default.aspx">Ownership Profile</a></li><li><a href="https://investors.adp.com/stock-information/analyst-coverage/default.aspx">Analyst Coverage</a></li>
	</ul></li><li class="has-children"><a href="https://investors.adp.com/investor-resources/contact-investor-relations/default.aspx">Investor Resources</a><ul class="level2">
		<li><a href="https://investors.adp.com/investor-resources/contact-investor-relations/default.aspx">Contact Investor Relations</a></li><li><a href="https://investors.adp.com/investor-resources/faqs/default.aspx">FAQs</a></li><li><a href="https://investors.adp.com/investor-resources/email-alerts/default.aspx">Email Alerts</a></li><li><a href="https://investors.adp.com/investor-resources/rss/default.aspx">RSS</a></li>
	</ul></li>
</ul></nav></span><span class='HeaderPaneDiv7'><div id="_ctrl0_ctl24_divModuleContainer" class="module module-search module-search--desktop" role="search">
    <div class="module_container module_container--outer">
        
        <div class="module_container module_container--inner">
            <span id="_ctrl0_ctl24_lblSearchText" class="module-search_text"></span>
            <input name="_ctrl0$ctl24$txtSearchInput" type="text" maxlength="256" id="_ctrl0_ctl24_txtSearchInput" class="module_input module-search_input" aria-label="Search query" placeholder="Search" value="" onkeypress="javascript:var key; if (window.event) { key = window.event.keyCode; } else if (e) { key = e.which; } else { return true; } if (key == 13) __doPostBack(&#39;_ctrl0$ctl24$btnSearch&#39;, &#39;&#39;); " />
            <input type="submit" name="_ctrl0$ctl24$btnSearch" value="Submit" id="_ctrl0_ctl24_btnSearch" class="module_button module-search_button" />
            
        </div>
    </div>
</div></span><span class='HeaderPaneDiv8'><div id="_ctrl0_ctl27_divModuleContainer" class="module module-search module-search--mobile" role="search">
    <div class="module_container module_container--outer">
        
        <div class="module_container module_container--inner">
            <span id="_ctrl0_ctl27_lblSearchText" class="module-search_text"></span>
            <input name="_ctrl0$ctl27$txtSearchInput" type="text" maxlength="256" id="_ctrl0_ctl27_txtSearchInput" class="module_input module-search_input" aria-label="Search query" placeholder="Search" value="" onkeypress="javascript:var key; if (window.event) { key = window.event.keyCode; } else if (e) { key = e.which; } else { return true; } if (key == 13) __doPostBack(&#39;_ctrl0$ctl27$btnSearch&#39;, &#39;&#39;); " />
            <input type="submit" name="_ctrl0$ctl27$btnSearch" value="Submit" id="_ctrl0_ctl27_btnSearch" class="module_button module-search_button" />
            
        </div>
    </div>
</div></span></span></div>
            </div>
            <div class="pane pane--banner grid--no-gutter">
                <div class="pane_inner"><span class='HeaderPane2Div9'><div id="_ctrl0_ctl30_divModuleContainer" class="module module-embed module-slider dark module-slider--banner">
    <div class="module_container module_container--outer">
        
        <div class="module_container module_container--inner">
            <div class="module_container module_container--content"></div>
<div class="slick-control-buttons">
    <div class="module-slick_nav"></div>
    <button type="button" class="module-toggle-play"><i class="q4-icon_pause"></i></button>
</div>
<script type="text/javascript" src="https://widgets.q4app.com/widgets/q4.apimashup.1.12.1.min.js"></script>
<script type="text/javascript">
$('.module-slider').apiMashup({
    showAllYears: true,
    itemContainer: '.module_container--content',
    contentSources: {
      
        "events": {
            type: 'events',
            tags: ['slider'],
            limit: 1,
            template: (
                /* beautify preserve:start */
                '<div class="module_item" data-source="{{contentSourceID}}"><div class="module_item-wrap">'+
                    '<div class="module_item-wrap-inner">'+
                    '<div class="module-slider_title"><h1>{{{title}}}</h1></div>'+
                    '<div class="module_links module_icons-svg module_icons-svg--inline list--reset">' +
                '{{#presentations}}' +
                    '<div class="module_presentation"><a href="{{docUrl}}" target="_blank" class="module_link module_presentation-link"> Presentation <span class="sr-only">(opens in new window)</span></a></div>' +
                '{{/presentations}}' +
                '{{#pressReleases}}' +
                    '<div class="module_news"><a href="{{url}}" target="_blank" class="module_link module_news-link">Press Release <span class="sr-only">(opens in new window)</span></a></div>' +
                '{{/pressReleases}}' +
                '<ul class="module_attachments">' +
                    '{{#docs}}{{^video}}' +
                        '<li class="module_attachment {{type}}">' +
                            '<a href="{{url}}" target="_blank" class="module_link module_attachment-link">{{title}} <span class="sr-only">(opens in new window)</span></a>' +
                        '</li>' +
                    '{{/video}}{{/docs}}' +
                '</ul>' +
                '{{#hasVideos}}<ul class="module_videos">'+
                    '{{#docs}}{{#video}}' +
                        '<li class="module_attachment {{type}}">' +
                            '<a href="{{url}}" target="_blank" class="module_link module_attachment-link">{{title}} <span class="sr-only">(opens in new window)</span></a>' +
                        '</li>' +
                    '{{/video}}{{/docs}}' +
                '</ul>{{/hasVideos}}'+
                '{{#financialReports}}' +
                    '<ul class="module_financials">' +
                        '{{#docs}}{{^duplicateWebcast}}' +
                            '<li>' +
                                '<a href="{{docUrl}}" target="_blank" class="module_link module_financial-link {{docCategory}} module_financial-link--{{docCategory}}"> {{docTitle}} <span class="sr-only">(opens in new window)</span></a>' +
                            '</li>' +
                        '{{/duplicateWebcast}}{{/docs}}' +
                    '</ul>' +
                '{{/financialReports}}' +
                '{{#webcast}}' +
                    '<div class="module_webcast"><a href="{{webcast}}" target="_blank" class="module_link module_webcast-link">Webcast <span class="sr-only">(opens in new window)</span></a></div>' +
                '{{/webcast}}' +

            '</div>' +

                    '<div class="module-slider_description">'+
                            '<div class="module_more">'+
                                '<a class="button button--arrow" href="{{url}}">' +
                                    '<span class="module_link-text">Learn More</span>' +
                                '</a>' +
                            '</div>'+
                        '</div>'+
                    '</div>'+
                    '</div>'+
                '</div>'
                /* beautify preserve:end */
            )
        },
   "downloads": {
            type: 'downloads',
            downloadType: 'Slider',
            tags: ['slider'],
            limit: 2,
            template: (
                /* beautify preserve:start */
                '<div class="module_item" data-source="{{contentSourceID}}">'+
                    '<div class="module_item-wrap">'+
                    '<div class="module_item-wrap-inner">'+
                        '<div class="module_item-wrap--inner">'+
                            '<div class="module-slider_title"><h1>{{{title}}}</h1></div>'+
                            '<div class="module-slider_description">{{{description}}}</div>'+
                        '</div>'+
                    '</div>'+
                    '</div>'+
                '</div>'
                /* beautify preserve:end */
            )
        },
        "financials": {
            type: 'financials',
            reportTypes: ['Annual Report'],
            limit: 1,
            docCategories: ['annual'],
            template: (
                /* beautify preserve:start */
                '<div class="module_item" data-source="{{contentSourceID}}"><div class="module_item-wrap">'+
                '<div class="module_item-wrap-inner">'+
                    '<div class="module-slider_description">' +
                            '<div class="module-slider_title">' +
                                '<h1>' +
                                    '<span>{{year}} {{type}}</span>' +
                                '</h1>' +
                            '</div>' +
                            '{{#docs}}'+
                             '<a class="button button--arrow" href="{{docUrl}}" target="_blank">' +
                                '<span class="module_link-text">Learn More</span>' +
                              '</a>' +
                            '{{/docs}}' +
                        '</div>' +
                    '</div>'+
                    '</div>'+
                '</div>'
                /* beautify preserve:end */
            )
        },
        "news": {
            type: 'news',
            tags: ['slider-news'],
            // titleLength: 50,
            limit: 1,
            template: (
                /* beautify preserve:start */
                '<div class="module_item" data-source="{{contentSourceID}}"><div class="module_item-wrap">'+
                    '<div class="module_item-wrap-inner">'+
                    '<div class="module-slider_title"><h1>{{{title}}}</h1></div>'+
                    '<div class="module-slider_description">'+
                            '<div class="module_more">'+
                                '<a class="button button--arrow" href="{{url}}">' +
                                    '<span class="module_link-text">Learn More</span>' +
                                '</a>' +
                            '</div>'+
                        '</div>'+
                    '</div>'+
                    '</div>'+
                '</div>'
                /* beautify preserve:end */
            )
        },
    },
    beforeRenderItems: function(e, data) {
        // order slides by content type through the below array
        var sortOrder = [ 'events', 'downloads', 'news', 'financials'];
        $.each(data.items, function(i, item) {
            item.sortBy = sortOrder.indexOf(item.contentSourceID);

            $.each(item.financialReports, function(j, report) {
                $.each(report.docs, function(k, doc) {
                    if (doc.docCategory == 'webcast' && doc.docUrl == item.webcast) {
                        doc.duplicateWebcast = true;
                    }
                    // if (doc.docCategory == 'webcast') {
                    //     doc.docTitle = 'Webcast Replay';
                    // }
                });
            });

        });
        data.items.sort(function(a, b) {
            if (a.sortBy < b.sortBy) return -1;
            if (a.sortBy > b.sortBy) return 1;
            return 0;
        });
        // remove duplicated webcast link


    },
    complete: function(e) {
        q4Defaults.addToCalendar('[data-source="events"]');
        $(e.target).find('.module_container--content').slick({
            slidesToShow: 1,
            slidesToScroll: 1,
            arrows: true,
            dots: true,
            fade: true,
            autoplay: false,
            autoplaySpeed: 7000,
            pauseOnHover: true,
            appendDots: '.module-slick_nav',
            responsive: [{
                breakpoint: 769,
                settings: {
                    dots: true,
                    arrows: false,
                    adaptiveHeight: false
                }
            }]

        });
        $('.module-toggle-play').on('click', function() {
            if (!$('.module-toggle-play').hasClass('js--play')) {
                $('.module-toggle-play').addClass('js--play');
                $('.module_container--content').slick('slickPause');
            } else {
                $('.module-toggle-play').removeClass('js--play');
                $('.module_container--content').slick('slickPlay');
            }
        });
    }
});
</script>
        </div>
    </div>
</div></span><span class='HeaderPane2Div10'><div id="_ctrl0_ctl33_divModuleContainer" class="module module-embed module-stock-header">
    <div class="module_container module_container--outer">
        
        <div class="module_container module_container--inner">
            <script src="https://widgets.q4app.com/widgets/q4.stockQuote.1.0.11.min.js"></script>
<script>
 $('.module-stock-header .module_container--inner').stockQuote({
    usePublic: GetViewType() != "0",
    apiKey: Q4ApiKey,
    changeCls: ['module-stock-header_down', 'module-stock-header_up'],
    stockTpl: (
        '{{#.}}' +
        '<div class="module-stock-values">'+
            '<span class="module-stock-header_description1">{{exchange}}: {{symbol}}</span>' +
            '<span class="module-stock-header_stock-price">{{tradePrice}}</span>' +
            '<span class="module-stock-header_change {{uod}}">' +
                '<span class="module-stock-header_indicator">{{uodSymbol}}</span>{{change}} ( {{percChange}}% )' +
            '</span>' +
        '</div>'+
            // '<span class="module-stock-header_volume-text">Volume: </span>' +
            // '<span class="module-stock-header_volume">{{volume}}</span>' +
        '<div class="module-stock-dates">'+
            '<span class="module-stock-header_description3">20 minutes minimum delay</span>' +
            '<span class="module-stock-header_date">{{tradeDate}}</span>' +
            '<span class="module-stock-header_time">{{tradeTime}}</span>' +
        '</div>'+
        '{{/.}}'
    ),
});
</script>
        </div>
    </div>
</div></span></div>
            </div>
            <div class="pane pane--navigation">
                <div class="pane_inner"><span class='NavigationPaneDiv11'><div id="_ctrl0_ctl36_divModuleContainer" class="module module-html module-corp-nav-mobile list--reset">
    <div class="module_container module_container--outer">
        
        <div class="module_container module_container--inner">
            <ul class="module-corp-nav-mobile_links">
    <li><a href="https://www.adp.com/what-we-offer.aspx">What We Offer</a></li>
    <li><a href="https://www.adp.com/who-we-serve.aspx">Who We Serve</a></li>
    <li><a href="https://www.adp.com/resources.aspx">Resources</a></li>
    <li><a href="https://www.adp.com/about-adp.aspx">About ADP</a></li>
</ul>
<div class="module-corp-nav-mobile_buttons">
    <button class="module-corp-nav-mobile_button module-corp-nav-mobile_button--search button" type="button">Search</button>
    <ul>
        <li class="module-corp-nav-mobile_button module-corp-nav-mobile_button--support"><a href="https://www.adp.com/contact-us/customer-service.aspx" class="button button--inverted">Support</a></li>
        <li class="module-corp-nav-mobile_button module-corp-nav-mobile_button--login"><a href="https://www.adp.com/logins.aspx" class="button button--red">Login</a></li>
    </ul>
</div>
        </div>
    </div>
</div></span></div>
            </div>
        </div>
        <div class="layout_content" id="maincontent">
            <div class="pane pane--breadcrumb">
                <div class="pane_inner"></div>
            </div>
            <div class="pane pane--left">
                <div class="pane_inner"><span class='LeftPaneDiv'><span class='LeftPaneDiv12'><nav class="nav--main-ir"><ul class="level1">
	<li class="selected"><a href="https://investors.adp.com/press-releases/default.aspx">Press Releases</a></li><li><a href="https://investors.adp.com/events-and-presentations/default.aspx">Events &amp; Presentations</a></li><li class="has-children"><a href="https://investors.adp.com/corporate-governance/board-of-directors/default.aspx">Corporate Governance</a><ul class="level2">
		<li><a href="https://www.adp.com/about-adp/leadership.aspx">Leadership Team</a></li><li><a href="https://investors.adp.com/corporate-governance/board-of-directors/default.aspx">Board of Directors</a></li><li><a href="https://investors.adp.com/corporate-governance/governance-documents/default.aspx">Governance Documents</a></li><li><a href="https://investors.adp.com/corporate-governance/committee-composition/default.aspx">Committee Composition</a></li><li><a href="https://www.adp.com/about-adp/corporate-social-responsibility/ethics.aspx">Code of Business Conduct and Ethics</a></li><li><a href="https://www.adp.com/about-adp/corporate-social-responsibility/ethics/code-of-ethics-for-principal-executive-officer-and-senior-financial-officers.aspx">Code of Ethics for Principal Executive Officer and Senior Financial Officer</a></li><li><a href="https://www.adp.com/about-adp/corporate-social-responsibility/ethics/anti-bribery-policy.aspx">Anti-Bribery Policy</a></li><li><a href="https://www.adp.com/about-adp/data-privacy.aspx">Data Privacy</a></li><li><a href="https://www.adp.com/about-adp/data-security.aspx">Data Security</a></li><li><a href="https://investors.adp.com/corporate-governance/contact-the-board/default.aspx">Contact the Board</a></li>
	</ul></li><li class="has-children"><a href="https://www.adp.com/about-adp/corporate-social-responsibility">CSR</a><ul class="level2">
		<li><a href="https://www.adp.com/about-adp/corporate-social-responsibility">CSR at ADP</a></li><li><a href="http://sustainability.adp.com/" target="_blank">Our CSR Report</a></li>
	</ul></li><li class="has-children"><a href="https://investors.adp.com/financial-information/sec-filings/default.aspx">Financial Information</a><ul class="level2">
		<li><a href="https://investors.adp.com/financial-information/sec-filings/default.aspx">SEC Filings</a></li><li><a href="https://investors.adp.com/financial-information/quarterly-results/default.aspx">Quarterly Results</a></li><li><a href="https://investors.adp.com/financial-information/annual-reports-and-proxies/default.aspx">Annual Reports &amp; Proxies</a></li><li><a href="https://investors.adp.com/financial-information/letter-to-shareholders/default.aspx">Letter to Shareholders</a></li><li><a href="//s23.q4cdn.com/483669984/files/doc_financials/2020/q2/ADP-2Q20-Supplemental-Schedule.pdf" target="_blank">Supplemental Financial Data</a></li>
	</ul></li><li class="has-children"><a href="https://investors.adp.com/stock-information/stock-quote-and-chart/default.aspx">Stock Information</a><ul class="level2">
		<li><a href="https://investors.adp.com/stock-information/stock-quote-and-chart/default.aspx">Stock Quote &amp; Chart</a></li><li><a href="https://investors.adp.com/stock-information/historical-price-lookup/default.aspx">Historical Price Lookup</a></li><li><a href="https://investors.adp.com/stock-information/investment-calculator/default.aspx">Investment Calculator</a></li><li><a href="https://investors.adp.com/stock-information/dividend-history/default.aspx">Dividend History</a></li><li><a href="https://investors.adp.com/stock-information/ownership-profile/default.aspx">Ownership Profile</a></li><li><a href="https://investors.adp.com/stock-information/analyst-coverage/default.aspx">Analyst Coverage</a></li>
	</ul></li><li class="has-children"><a href="https://investors.adp.com/investor-resources/contact-investor-relations/default.aspx">Investor Resources</a><ul class="level2">
		<li><a href="https://investors.adp.com/investor-resources/contact-investor-relations/default.aspx">Contact Investor Relations</a></li><li><a href="https://investors.adp.com/investor-resources/faqs/default.aspx">FAQs</a></li><li><a href="https://investors.adp.com/investor-resources/email-alerts/default.aspx">Email Alerts</a></li><li><a href="https://investors.adp.com/investor-resources/rss/default.aspx">RSS</a></li>
	</ul></li>
</ul></nav></span></span></div>
            </div>
            <div class="pane pane--content">
                <div class="pane_inner"><span class='ContentPaneDiv'><span class='ContentPaneDiv1'><div id="_ctrl0_ctl66_divModuleContainer" class="module module-embed module-news--widget">
    <div class="module_container module_container--outer">
        <h2 id="_ctrl0_ctl66_lblTitle" class="module_title"><span id="_ctrl0_ctl66_lblModuleTitle" class="ModuleTitle">Press Releases</span></h2>
        <div class="module_container module_container--inner">
            <div class="module_container module_container--content">
    <div class="module_rss module_rss--top">
        <a href="/rss/PressRelease.aspx" class="module_rss-link" target="_blank">
            <i class="q4-icon_rss" aria-hidden="true"></i>
            <span class="sr-only">Press Release RSS Feed (opens in new window)</span>
        </a>
    </div>
    <select class="module-years dropdown module_options-select"></select>
    <div class="module_item-container"></div>
</div>
<ul class="module_pagination"></ul>
<script type="text/javascript" src="https://widgets.q4app.com/widgets/q4.pager.1.2.0.min.js"></script>
<script>
$('.module-news--widget .module_container--content').news({
    //showAllYears: true,
    dateFormat: 'M dd, yy',
    allYearsText: 'Year',
    yearSelect: '.module-years',
    yearContainer: '.module-years',
    yearTemplate: '<option value="{{value}}">{{year}}</option>',
    itemContainer: '.module_item-container',
    loadShortBody: true,
    shortBodyLength: 200,
    itemNotFoundMessage: '<div class="module-not-found-message"><i class="q4-icon_warning-line"></i> There are no press releases to display at this time.</div>',
    itemTemplate: (
        '<div class="module_item grid--no-gutter">' +
            '<div class="module_date-time">' +
                '<span class="module_date-text">{{date}}</span> ' +
            '</div>' +
                '<div class="module_headline">' +
                '<a class="module_headline-link" href="{{url}}">{{title}}</a>' +
                '</div>' +
                '<div class="module_links module_icons-svg module_icons-svg--inline">'+
                  '{{#docUrl}}'+
                        '<a href="{{docUrl}}" class="module_link" target="_blank">'+
                            '<span class="module_link-text">Download</span>'+
                            '<span class="sr-only">PDF format download (opens in new window)</span>'+
                        '</a>'+
                    '{{/docUrl}}'+
                '</div>'+
          '</div>'
    )

});
</script>
        </div>
    </div>
</div></span></span></div>
            </div>
            <div class="pane pane--right">
                <div class="pane_inner"><span class='RightPaneDiv'></span></div>
            </div>
        </div>
        <div class="layout_footer" role="contentinfo">
            <div class="pane pane--footer grid">
                <div class="pane_inner"><span class='FooterPaneDiv'><span class='FooterPaneDiv13'><div id="_ctrl0_ctl42_RightBlock" class="hidden"></div>
<div id="_ctrl0_ctl42_divModuleContainer" class="module module-links  list--reset grid_col grid_col--3-of-12 grid_col--md-1-of-1">
    <div class="module_container module_container--outer">
        <h2 id="_ctrl0_ctl42_lblTitle" class="module_title"><span id="_ctrl0_ctl42_lblModuleTitle" class="ModuleTitle">Quick Links</span></h2>
        <div class="module_container module_container--inner">
            <ul id="_ctrl0_ctl42_qlList" class="module-links_list">
                
                        <li id="_ctrl0_ctl42_QuickLinkList_ctl00_liQuickLink" class="QuickLinkRow">
                            
                            
                            <a href="/investor-resources/faqs/default.aspx" id="_ctrl0_ctl42_QuickLinkList_ctl00_link" class="module-links_list-item-link">FAQs</a>
                            
                        </li>
                    
                        <li id="_ctrl0_ctl42_QuickLinkList_ctl01_liQuickLink" class="QuickLinkRowAlt">
                            
                            
                            <a href="/financial-information/letter-to-shareholders/default.aspx" id="_ctrl0_ctl42_QuickLinkList_ctl01_link" class="module-links_list-item-link">Letter to Shareholders</a>
                            
                        </li>
                    
            </ul>
        </div>
    </div>
</div></span><span class='FooterPaneDiv14'><div id="_ctrl0_ctl45_divModuleContainer" class="module module-subscribe module-subscribe--fancy module-subscribe--footer grid_col grid_col--6-of-12 grid_col--md-1-of-1">
    <div class="module_container module_container--outer">
        <h2 id="_ctrl0_ctl45_lblTitle" class="module_title"><span id="_ctrl0_ctl45_lblModuleTitle" class="ModuleTitle">Email Alerts</span><span id="_ctrl0_ctl45_lblHelpPage"></span></h2>
        <div class="module_container module_container--inner">
            <div class="module_introduction"><span id="_ctrl0_ctl45_lblIntroText" class="IntroText"><p>To opt-in for investor email alerts, please enter your email address in the field below and select at least one alert option. After submitting your request, you will receive an activation email to the requested email address. You must click the activation link in order to complete your subscription. You can sign up for additional alert options at any time.</p><p>At Automatic Data Processing, we promise to treat your data with respect and will not share your information with any third party. You can unsubscribe to any of the investor alerts you are subscribed to by visiting the ‘unsubscribe’ section below. If you experience any issues with this process, please contact us for further assistance.</p><p><strong>By providing your email address below, you are providing consent to Automatic Data Processing to send you the requested Investor Email Alert updates.</strong></p><p class="module_required-text">* Required</p></span></div>
            <div id="_ctrl0_ctl45_validationsummary" class="module_error-container" style="display:none;">

</div>
            <table class="module-subscribe_table module-subscribe_form">
                
                
                <tr id="_ctrl0_ctl45_rowEmailAddress" class="module-subscribe_table-input module-subscribe_email">
	<td id="_ctrl0_ctl45_ctl02">
                        <label for="_ctrl0_ctl45_txtEmail" id="_ctrl0_ctl45_lblEmailAddressText">Email</label>
                        <span id="_ctrl0_ctl45_lblRequiredEmailAddress" class="module_required">*</span>
                        <input name="_ctrl0$ctl45$txtEmail" type="text" maxlength="128" id="_ctrl0_ctl45_txtEmail" class="module_input" placeholder="" />
                        <span id="_ctrl0_ctl45_regexEmailValidator1" style="display:none;"></span>
                        <span id="_ctrl0_ctl45_reqvalEmailValidator1" style="display:none;"></span>
                    </td>
</tr>

                
                
                
                
                
                
                
                
                
                
                
                
                
                
            </table>
            <table id="_ctrl0_ctl45_tableMailingLists" class="module-subscribe_table module-subscribe_mailing-list">
	<tr id="_ctrl0_ctl45_rowMailingListLabel" class="module-subscribe_table-input module-subscribe_list-header">
		<td id="_ctrl0_ctl45_ctl17">
                        <label for="_ctrl0_ctl45_chkLists" id="_ctrl0_ctl45_lblMailingListsText">Mailing Lists</label>
                        <span id="_ctrl0_ctl45_lblRequiredMailingLists" class="module_required">*</span>
                    </td>
	</tr>
	<tr id="_ctrl0_ctl45_rowMailingLists" class="module-subscribe_table-input module-subscribe_list">
		<td id="_ctrl0_ctl45_ctl18">
                        <table id="_ctrl0_ctl45_chkLists">
			<tr>
				<td><input id="_ctrl0_ctl45_chkLists_0" type="checkbox" name="_ctrl0$ctl45$chkLists$0" value="31" /><label for="_ctrl0_ctl45_chkLists_0">Press Releases</label></td>
			</tr><tr>
				<td><input id="_ctrl0_ctl45_chkLists_1" type="checkbox" name="_ctrl0$ctl45$chkLists$1" value="33" /><label for="_ctrl0_ctl45_chkLists_1">Events & Presentations</label></td>
			</tr><tr>
				<td><input id="_ctrl0_ctl45_chkLists_2" type="checkbox" name="_ctrl0$ctl45$chkLists$2" value="35" /><label for="_ctrl0_ctl45_chkLists_2">SEC Filings</label></td>
			</tr><tr>
				<td><input id="_ctrl0_ctl45_chkLists_3" type="checkbox" name="_ctrl0$ctl45$chkLists$3" value="36" /><label for="_ctrl0_ctl45_chkLists_3">Stock Information</label></td>
			</tr>
		</table>
                        
                        <span id="_ctrl0_ctl45_cusvalMailingListsValidator" style="display:none;"></span>
                    </td>
	</tr>
</table>

            <div id="_ctrl0_ctl45_UCCaptcha_divModuleContainer" class="CaptchaContainer">
<table id="_ctrl0_ctl45_UCCaptcha_Table1" cellpadding="0" cellspacing="0" border="0" width="100%">
	<tr id="_ctrl0_ctl45_UCCaptcha_ctl00">
		<td id="_ctrl0_ctl45_UCCaptcha_ctl01" colspan="2">&nbsp;</td>
	</tr>
	<tr id="_ctrl0_ctl45_UCCaptcha_ctl02">
		<td id="_ctrl0_ctl45_UCCaptcha_ctl03" colspan="2"><img src="https://investors.adp.com/q4api/v4/captcha?clientId=_ctrl0_ctl45_UCCaptcha" id="_ctrl0_ctl45_UCCaptcha_Image1" /></td>
	</tr>
	<tr id="_ctrl0_ctl45_UCCaptcha_ctl04">
		<td id="_ctrl0_ctl45_UCCaptcha_ctl05" colspan="2"><b>Enter the code shown above.</b></td>
	</tr>
	<tr id="_ctrl0_ctl45_UCCaptcha_ctl06">
		<td id="_ctrl0_ctl45_UCCaptcha_ctl07" colspan="2">
			<input name="_ctrl0$ctl45$UCCaptcha$txtCode" type="text" id="_ctrl0_ctl45_UCCaptcha_txtCode" /><span id="_ctrl0_ctl45_UCCaptcha_RequiredFieldValidator1" style="display:none;">*</span>
		</td>
	</tr>
</table>

</div>
            <div class="module_actions">
                <input type="submit" name="_ctrl0$ctl45$btnSubmit" value="Submit" onclick="javascript:WebForm_DoPostBackWithOptions(new WebForm_PostBackOptions(&quot;_ctrl0$ctl45$btnSubmit&quot;, &quot;&quot;, true, &quot;4378043b-b1b6-41af-b181-b523c287119f&quot;, &quot;&quot;, false, false))" id="_ctrl0_ctl45_btnSubmit" class="button module-subscribe_submit-button" />
            </div>
        </div>
    </div>
</div>
<div id="_ctrl0_ctl45_divEditSubscriberConfirmation" class="module module-subscribe module_confirmation-container" style="DISPLAY:none;">
    <div class="module_container module_container--outer">
        <h2 class="module_title">Email Alert Sign Up Confirmation</h2>
        <div class="module_container module_container--inner">
            
        </div>
    </div>
</div></span><span class='FooterPaneDiv15'><div id="_ctrl0_ctl48_divModuleContainer" class="module module-html module-contact grid_col grid_col--3-of-12 grid_col--md-1-of-1">
    <div class="module_container module_container--outer">
        <h2 id="_ctrl0_ctl48_lblTitle" class="module_title"><span id="_ctrl0_ctl48_lblModuleTitle" class="ModuleTitle">IR Contact</span></h2>
        <div class="module_container module_container--inner">
            <p>
    <span class="module-phone"><i class="q4-icon_phone"></i>973-974-5858</span>
    <a href="mailto:investor.mail@adp.com"><i class="q4-icon_mail"></i> <span>investor.mail@adp.com</span></a>
</p>
        </div>
    </div>
</div></span><span class='FooterPaneDiv16'><div id="_ctrl0_ctl51_RightBlock" class="hidden"></div>
<div id="_ctrl0_ctl51_divModuleContainer" class="module module-links module-links-investors js--hidden">
    <div class="module_container module_container--outer">
        
        <div class="module_container module_container--inner">
            <ul id="_ctrl0_ctl51_qlList" class="module-links_list">
                
                        <li id="_ctrl0_ctl51_QuickLinkList_ctl00_liQuickLink" class="QuickLinkRow">
                            
                            
                            <a href="/overview/default.aspx" id="_ctrl0_ctl51_QuickLinkList_ctl00_link" class="module-links_list-item-link">Overview</a>
                            
                        </li>
                    
                        <li id="_ctrl0_ctl51_QuickLinkList_ctl01_liQuickLink" class="QuickLinkRowAlt">
                            
                            
                            <a href="https://www.adp.com/about-adp/corporate-social-responsibility" id="_ctrl0_ctl51_QuickLinkList_ctl01_link" class="module-links_list-item-link" target="_blank">CSR</a>
                            
                        </li>
                    
                        <li id="_ctrl0_ctl51_QuickLinkList_ctl02_liQuickLink" class="QuickLinkRow">
                            
                            
                            <a href="/press-releases/default.aspx" id="_ctrl0_ctl51_QuickLinkList_ctl02_link" class="module-links_list-item-link">Press Releases</a>
                            
                        </li>
                    
                        <li id="_ctrl0_ctl51_QuickLinkList_ctl03_liQuickLink" class="QuickLinkRowAlt">
                            
                            
                            <a href="/financial-information/sec-filings/default.aspx" id="_ctrl0_ctl51_QuickLinkList_ctl03_link" class="module-links_list-item-link">Financial Information</a>
                            
                        </li>
                    
                        <li id="_ctrl0_ctl51_QuickLinkList_ctl04_liQuickLink" class="QuickLinkRow">
                            
                            
                            <a href="/events-and-presentations/default.aspx" id="_ctrl0_ctl51_QuickLinkList_ctl04_link" class="module-links_list-item-link">Events & Presentation</a>
                            
                        </li>
                    
                        <li id="_ctrl0_ctl51_QuickLinkList_ctl05_liQuickLink" class="QuickLinkRowAlt">
                            
                            
                            <a href="/stock-information/stock-quote-and-chart/default.aspx" id="_ctrl0_ctl51_QuickLinkList_ctl05_link" class="module-links_list-item-link">Stock Information</a>
                            
                        </li>
                    
                        <li id="_ctrl0_ctl51_QuickLinkList_ctl06_liQuickLink" class="QuickLinkRow">
                            
                            
                            <a href="/corporate-governance" id="_ctrl0_ctl51_QuickLinkList_ctl06_link" class="module-links_list-item-link">Corporate Governance</a>
                            
                        </li>
                    
                        <li id="_ctrl0_ctl51_QuickLinkList_ctl07_liQuickLink" class="QuickLinkRowAlt">
                            
                            
                            <a href="/investor-resources/contact-investor-relations/default.aspx" id="_ctrl0_ctl51_QuickLinkList_ctl07_link" class="module-links_list-item-link">Investor Resources</a>
                            
                        </li>
                    
            </ul>
        </div>
    </div>
</div></span></span></div>
            </div>
            <div class="pane pane--footer2">
                <div class="pane_inner"><span class='FooterPane2Div17'><div id="_ctrl0_ctl54_divModuleContainer" class="module module-html module-footer dark">
    <div class="module_container module_container--outer">
        
        <div class="module_container module_container--inner">
            <div class="grid module-footer_top">
    <div class="grid_col grid_col--3-of-12 grid_col--md-1-of-1 grid_col--sm-1-of-1">
        <a href="https://www.adp.com/"><img src="//s23.q4cdn.com/483669984/files/design/ADP-logo-white.svg" alt="Automatic Data Processing Logo"></a>
        <div class="module-contact">
            <h4>Contact Sales</h4>
            <p>800-225-5237</p>
            <a href="https://www.adp.com/logins.aspx" class="button button--small button--red">Login</a>
        </div>
    </div>
    <div class="grid_col grid_col--9-of-12 grid_col--md-1-of-1 grid_col--sm-1-of-1 module-right">
        <div class="module-corp-nav">
            <ul>
                <li><a href="https://www.adp.com/what-we-offer.aspx">What We Offer</a></li>
                <li><a href="https://www.adp.com/who-we-serve.aspx">Who We Serve</a></li>
                <li><a href="https://www.adp.com/resources.aspx">Resources</a></li>
                <li><a href="https://www.adp.com/about-adp.aspx">About ADP</a></li>
            </ul>
        </div>
        <div class="module-ir-nav">
            <h3>Investor Relations</h3>
            <div class="module_container"></div>
        </div>
    </div>
</div>
<div class="grid module-footer_bottom">
    <div class="grid_col grid_col--3-of-12 grid_col--md-1-of-1 grid_col--sm-1-of-1">
        <ul class="region-links">
            <li class="region-selector">
                <a class="select-link" tabindex="0"><span class="flag-icon flag-icon-us"></span>United States</a>
                <ul class="region-options">
                    <li>
                        <a href="http://www.adp-ar.com"><span class="flag-icon flag-icon-ar"></span>Argentina</a>
                    </li>
                    <li>
                        <a href="http://www.adppayroll.com.au/"><span class="flag-icon flag-icon-au"></span>Australia</a>
                    </li>
                    <li>
                        <a href="http://www.adp.com.br/"><span class="flag-icon flag-icon-br"></span>Brazil</a>
                    </li>
                    <li>
                        <a href="http://www.adp.ca/en-ca/default.aspx"><span class="flag-icon flag-icon-ca"></span>Canada (English)</a>
                    </li>
                    <li>
                        <a href="http://www.adp.ca/fr-ca/default.aspx"><span class="flag-icon flag-icon-ca"></span>Canada (French)</a>
                    </li>
                    <li>
                        <a href="http://adp.cl"><span class="flag-icon flag-icon-cl"></span>Chile</a>
                    </li>
                    <li>
                        <a href="http://www.adpchina.com/"><span class="flag-icon flag-icon-cn"></span>China</a>
                    </li>
                    <li>
                        <a href="http://www.fr.adp.com/"><span class="flag-icon flag-icon-fr"></span>France</a>
                    </li>
                    <li>
                        <a href="http://www.de-adp.com/"><span class="flag-icon flag-icon-de"></span>Germany</a>
                    </li>
                    <li>
                        <a href="http://www.adp.com.hk/"><span class="flag-icon flag-icon-hk"></span>Hong Kong</a>
                    </li>
                    <li>
                        <a href="http://www.adp.in/"><span class="flag-icon flag-icon-in"></span>India</a>
                    </li>
                    <li>
                        <a href="http://www.it-adp.com/"><span class="flag-icon flag-icon-it"></span>Italy</a>
                    </li>
                    <li>
                        <a href="http://www.adp.nl/"><span class="flag-icon flag-icon-nl"></span>Netherlands</a>
                    </li>
                    <li>
                        <a href="http://www.adp.pe/"><span class="flag-icon flag-icon-pe"></span>Peru</a>
                    </li>
                    <li>
                        <a href="http://www.adp.ph/"><span class="flag-icon flag-icon-ph"></span>Philippines</a>
                    </li>
                    <li>
                        <a href="http://www.adp.pl/"><span class="flag-icon flag-icon-pl"></span>Poland</a>
                    </li>
                    <li>
                        <a href="http://www.adp.sg/"><span class="flag-icon flag-icon-sg"></span>Singapore</a>
                    </li>
                    <li>
                        <a href="http://www.es-adp.com"><span class="flag-icon flag-icon-es"></span>Spain</a>
                    </li>
                    <li>
                        <a href="http://www.adp.ch/"><span class="flag-icon flag-icon-ch"></span>Switzerland</a>
                    </li>
                    <li>
                        <a href="http://www.adp.co.uk/"><span class="flag-icon flag-icon-gb"></span>United Kingdom</a>
                    </li>
                    <li>
                        <a href="https://www.adp.com/" rel="region-link current-selection" target=""><span class="flag-icon flag-icon-us"></span>United States</a>
                    </li>
                </ul>
            </li>
        </ul>
        <p>All Worldwide Locations</p>
    </div>
    <div class="grid_col grid_col--9-of-12 grid_col--md-1-of-1 grid_col--sm-1-of-1 module-right">
        <ul id="social-icons" class="sm-links clearfix">
            <li><a href="https://www.facebook.com/AutomaticDataProcessing/" target="_blank" class="sm-icn sm-icn-facebook">facebook</a></li>
            <li><a href="https://twitter.com/adp" target="_blank" class="sm-icn sm-icn-twitter">twitter</a></li>
            <li><a href="https://www.youtube.com/user/adp" target="_blank" class="sm-icn sm-icn-youtube">youtube</a></li>
            <li><a href="https://www.linkedin.com/company/adp" target="_blank" class="sm-icn sm-icn-linkedin">LinkedIn</a></li>
            <li><a href="https://plus.google.com/113704408436778247421" target="_blank" class="sm-icn sm-icn-googleplus">google plus </a></li>
        </ul>
        <ul class="legal-links">
            <li><a href="https://www.adp.com/legal.aspx">Terms</a></li>
            <li><a href="https://www.adp.com/site-map.aspx">Site Map</a></li>
            <li><a href="https://www.adp.com/privacy.aspx">Privacy</a></li>
            <li><a href="https://www.adp.com/modern-slavery-statement.aspx">Modern Slavery Statement</a></li>
        </ul>
        <p class="module-footer--footnote">ADP, the ADP logo and ADP A more human resource are registered trademarks of ADP, LLC. All other marks are the property of their respective owners.</p>
    </div>
</div>
        </div>
    </div>
</div></span></div>
            </div>
            <div class="pane pane--credits">
                <div class="pane_inner"><span class='Q4FooterDiv18'><div id="_ctrl0_ctl57_divModuleContainer" class="module module-html copyright">
    <div class="module_container module_container--outer">
        
        <div class="module_container module_container--inner">
            © <span class="copyright_year"></span> ADP - All rights reserved
        </div>
    </div>
</div></span><span class='Q4FooterDiv19'>
<div class="module module-q4-credits">
    <div class="module_container module_container--outer">
        <div class="module_container module_container--inner">
            <a href="https://www.q4inc.com/Powered-by-Q4/" id="_ctrl0_ctl60_hrefWebsiteRecording" class="module-q4-credits-link" target="_blank">
                <span id="_ctrl0_ctl60_lblWebsiteRecording" class="module-q4-credits_powered-text">Powered By Q4 Inc.</span>
                <span id="_ctrl0_ctl60_lblVersion" class="module-q4-credits_version-text">5.31.1.1</span>
                <span class="sr-only">(opens in new window)</span>
            </a>
        </div>
    </div>
</div></span><span class='Q4FooterDiv20'><div id="_ctrl0_ctl63_divModuleContainer" class="module module-embed hidden">
    <div class="module_container module_container--outer">
        
        <div class="module_container module_container--inner">
            <script>
var q4App = $.extend(true, q4Defaults, {
    options: {
        headerOffset: $('.pane--header').outerHeight()
    },
    init: function() {
        var app = this;

        app.cleanUp();
        app.submitOnEnter('.module-unsubscribe');
        app.submitOnEnter('.module-search');
        app.validateSubmit('.module-search');
        app.superfish($('.nav--main .level1'), { cssArrows: false });
        app.mobileMenuToggle($('.layout'), '.pane--navigation', '.module-toggle_button');
        app.cleanQuickLinks($('.module-links'));
        app.copyright($('.copyright_year'));
        app.reveal('.layout', '.module-header-item--search-icon', '.module-search--desktop', false, '', '', 'js--revealed ');
        app.reveal('.layout', '.module-nav-ir_toggle-button', '.pane--left', false, '', 'js--active', 'js--open');
        app.docTracking();
        app.fancySignup();
        app.resetDate(['.nav a[href*="s3.q4web.com"]:not([href$=".pdf"])']);
        app.previewToolbar();
        app.sections();
        app.contrast.init();
        app.toggleLocations();
        app.appendInvestorLinks();
        app.appendArrow();
        app.scrollNav();
        app.removeToggleClassMobile();
        app.initSelect2();
    },
    scrollNav: function() {
        $(window).on('scroll', function() {
            if ($(window).scrollTop() > 0) {
                $('.layout').addClass('js--scroll')
            } else {
                $('.layout').removeClass('js--scroll');
            }
        });

    },
    removeToggleClassMobile:function(){
        $('.module-corp-nav-mobile_button--search').on('click', function() {
            $('.layout').removeClass('js--mobile');
            $('.layout').addClass('js--open-search');
        });
        $('.module-toggle--mobile').on('click', function() {
            $('.layout').removeClass('js--open-search');
        });
        $('.module-search_text').on('click', function() {
            $('.layout').removeClass('js--open-search');
        });
    },
    toggleLocations: function() {
        $('.select-link').on('click', function() {
            $(this).parent().toggleClass('js--active');
        });
    },
    appendInvestorLinks: function() {
        var linksIr = $('.module-links-investors .module_container--inner').html();
        $('.module-ir-nav .module_container').append(linksIr);
    },
    appendArrow: function() {
        $('.pane--left .nav--main-ir .level1 > li.has-children').append('<span class="q4-icon_chevron-down"></span>');
        $('.pane--left .nav--main-ir .level1 > li.has-children > span').on('click', function() {
            $(this).parent().toggleClass('js--open');
        });
        $('.module-corp-nav-mobile li.has-children > a').append('<span class="q4-icon_plus"></span>');
    },
    initSelect2: function() {
        $('select').not('.PreviewToolBar select').select2({
            minimumResultsForSearch: Infinity
        });
    },
    scollingTable: function(selector){
        $(selector).not(selector+' table').wrap('<div class="table-wrapper" />');
    },

});
q4App.init();
</script>
        </div>
    </div>
</div></span><span class='Q4FooterDiv2'><div id="_ctrl0_ctl69_divModuleContainer" class="module module-embed">
    <div class="module_container module_container--outer">
        
        <div class="module_container module_container--inner">
            <script type="text/javascript">
q4App.makeSelect($('.module-news .module_nav'));
</script>
        </div>
    </div>
</div></span></div>
            </div>
        </div>
    </div>
</div>
                    <input type="hidden" name="__antiCSRF" id="__antiCSRF" value=""/>
                
<script type="text/javascript">
//<![CDATA[
var Page_ValidationSummaries =  new Array(document.getElementById("_ctrl0_ctl45_validationsummary"));
var Page_Validators =  new Array(document.getElementById("_ctrl0_ctl45_regexEmailValidator1"), document.getElementById("_ctrl0_ctl45_reqvalEmailValidator1"), document.getElementById("_ctrl0_ctl45_cusvalMailingListsValidator"), document.getElementById("_ctrl0_ctl45_UCCaptcha_RequiredFieldValidator1"));
//]]>
</script>

<script type="text/javascript">
//<![CDATA[
var _ctrl0_ctl45_validationsummary = document.all ? document.all["_ctrl0_ctl45_validationsummary"] : document.getElementById("_ctrl0_ctl45_validationsummary");
_ctrl0_ctl45_validationsummary.headertext = "<p class=\'module_message module_message--error\'>The following errors must be corrected:</p>";
_ctrl0_ctl45_validationsummary.displaymode = "List";
_ctrl0_ctl45_validationsummary.validationGroup = "4378043b-b1b6-41af-b181-b523c287119f";
var _ctrl0_ctl45_regexEmailValidator1 = document.all ? document.all["_ctrl0_ctl45_regexEmailValidator1"] : document.getElementById("_ctrl0_ctl45_regexEmailValidator1");
_ctrl0_ctl45_regexEmailValidator1.controltovalidate = "_ctrl0_ctl45_txtEmail";
_ctrl0_ctl45_regexEmailValidator1.errormessage = "Email address is not valid.";
_ctrl0_ctl45_regexEmailValidator1.display = "None";
_ctrl0_ctl45_regexEmailValidator1.validationGroup = "4378043b-b1b6-41af-b181-b523c287119f";
_ctrl0_ctl45_regexEmailValidator1.evaluationfunction = "RegularExpressionValidatorEvaluateIsValid";
_ctrl0_ctl45_regexEmailValidator1.validationexpression = "^([a-zA-Z0-9_\\-\\.]+)@((\\[[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.)|(([a-zA-Z0-9\\-]+\\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\\]?)$";
var _ctrl0_ctl45_reqvalEmailValidator1 = document.all ? document.all["_ctrl0_ctl45_reqvalEmailValidator1"] : document.getElementById("_ctrl0_ctl45_reqvalEmailValidator1");
_ctrl0_ctl45_reqvalEmailValidator1.controltovalidate = "_ctrl0_ctl45_txtEmail";
_ctrl0_ctl45_reqvalEmailValidator1.errormessage = "Email address is required.";
_ctrl0_ctl45_reqvalEmailValidator1.display = "None";
_ctrl0_ctl45_reqvalEmailValidator1.validationGroup = "4378043b-b1b6-41af-b181-b523c287119f";
_ctrl0_ctl45_reqvalEmailValidator1.evaluationfunction = "RequiredFieldValidatorEvaluateIsValid";
_ctrl0_ctl45_reqvalEmailValidator1.initialvalue = "";
var _ctrl0_ctl45_cusvalMailingListsValidator = document.all ? document.all["_ctrl0_ctl45_cusvalMailingListsValidator"] : document.getElementById("_ctrl0_ctl45_cusvalMailingListsValidator");
_ctrl0_ctl45_cusvalMailingListsValidator.errormessage = "Mailing list selection is required.";
_ctrl0_ctl45_cusvalMailingListsValidator.display = "None";
_ctrl0_ctl45_cusvalMailingListsValidator.validationGroup = "4378043b-b1b6-41af-b181-b523c287119f";
_ctrl0_ctl45_cusvalMailingListsValidator.evaluationfunction = "CustomValidatorEvaluateIsValid";
var _ctrl0_ctl45_UCCaptcha_RequiredFieldValidator1 = document.all ? document.all["_ctrl0_ctl45_UCCaptcha_RequiredFieldValidator1"] : document.getElementById("_ctrl0_ctl45_UCCaptcha_RequiredFieldValidator1");
_ctrl0_ctl45_UCCaptcha_RequiredFieldValidator1.controltovalidate = "_ctrl0_ctl45_UCCaptcha_txtCode";
_ctrl0_ctl45_UCCaptcha_RequiredFieldValidator1.focusOnError = "t";
_ctrl0_ctl45_UCCaptcha_RequiredFieldValidator1.errormessage = "Please provide the code.";
_ctrl0_ctl45_UCCaptcha_RequiredFieldValidator1.display = "Dynamic";
_ctrl0_ctl45_UCCaptcha_RequiredFieldValidator1.validationGroup = "4378043b-b1b6-41af-b181-b523c287119f";
_ctrl0_ctl45_UCCaptcha_RequiredFieldValidator1.evaluationfunction = "RequiredFieldValidatorEvaluateIsValid";
_ctrl0_ctl45_UCCaptcha_RequiredFieldValidator1.initialvalue = "";
//]]>
</script>


<script type="text/javascript">
//<![CDATA[

var Page_ValidationActive = false;
if (typeof(ValidatorOnLoad) == "function") {
    ValidatorOnLoad();
}

function ValidatorOnSubmit() {
    if (Page_ValidationActive) {
        return ValidatorCommonOnSubmit();
    }
    else {
        return true;
    }
}
        //]]>
</script>
</form>
            </div>
        </div>
    </div>
    
    <script type="text/javascript" src="/js/anti-csrf.js">
    </script>
</body>
</html>
