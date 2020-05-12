<!DOCTYPE HTML>
<html xmlns="http://www.w3.org/1999/xhtml" lang="en-US" xml:lang="en-US">
<head><title>
	Barrick Gold Corporation - News
</title><meta content="text/html; charset=UTF-8" http-equiv="Content-type" /><meta content="RevealTrans(Duration=0,Transition=0)" http-equiv="Page-Enter" /><meta content="IE=edge,chrome=1" http-equiv="X-UA-Compatible" /><script type="text/javascript">window.NREUM||(NREUM={});NREUM.info = {"beacon":"bam.nr-data.net","errorBeacon":"bam.nr-data.net","licenseKey":"4b6f7f959c","applicationID":"229922501","transactionName":"b1xWMUIDWBdWARFYX1YWdTZgTVIBUQMQXUQWWEcVSA==","queueTime":0,"applicationTime":889,"agent":"","atts":""}</script><script type="text/javascript">(window.NREUM||(NREUM={})).loader_config={licenseKey:"4b6f7f959c",applicationID:"229922501"};window.NREUM||(NREUM={}),__nr_require=function(e,n,t){function r(t){if(!n[t]){var i=n[t]={exports:{}};e[t][0].call(i.exports,function(n){var i=e[t][1][n];return r(i||n)},i,i.exports)}return n[t].exports}if("function"==typeof __nr_require)return __nr_require;for(var i=0;i<t.length;i++)r(t[i]);return r}({1:[function(e,n,t){function r(){}function i(e,n,t){return function(){return o(e,[u.now()].concat(f(arguments)),n?null:this,t),n?void 0:this}}var o=e("handle"),a=e(4),f=e(5),c=e("ee").get("tracer"),u=e("loader"),s=NREUM;"undefined"==typeof window.newrelic&&(newrelic=s);var p=["setPageViewName","setCustomAttribute","setErrorHandler","finished","addToTrace","inlineHit","addRelease"],l="api-",d=l+"ixn-";a(p,function(e,n){s[n]=i(l+n,!0,"api")}),s.addPageAction=i(l+"addPageAction",!0),s.setCurrentRouteName=i(l+"routeName",!0),n.exports=newrelic,s.interaction=function(){return(new r).get()};var m=r.prototype={createTracer:function(e,n){var t={},r=this,i="function"==typeof n;return o(d+"tracer",[u.now(),e,t],r),function(){if(c.emit((i?"":"no-")+"fn-start",[u.now(),r,i],t),i)try{return n.apply(this,arguments)}catch(e){throw c.emit("fn-err",[arguments,this,e],t),e}finally{c.emit("fn-end",[u.now()],t)}}}};a("actionText,setName,setAttribute,save,ignore,onEnd,getContext,end,get".split(","),function(e,n){m[n]=i(d+n)}),newrelic.noticeError=function(e,n){"string"==typeof e&&(e=new Error(e)),o("err",[e,u.now(),!1,n])}},{}],2:[function(e,n,t){function r(e,n){var t=e.getEntries();t.forEach(function(e){"first-paint"===e.name?c("timing",["fp",Math.floor(e.startTime)]):"first-contentful-paint"===e.name&&c("timing",["fcp",Math.floor(e.startTime)])})}function i(e,n){var t=e.getEntries();t.length>0&&c("lcp",[t[t.length-1]])}function o(e){if(e instanceof s&&!l){var n,t=Math.round(e.timeStamp);n=t>1e12?Date.now()-t:u.now()-t,l=!0,c("timing",["fi",t,{type:e.type,fid:n}])}}if(!("init"in NREUM&&"page_view_timing"in NREUM.init&&"enabled"in NREUM.init.page_view_timing&&NREUM.init.page_view_timing.enabled===!1)){var a,f,c=e("handle"),u=e("loader"),s=NREUM.o.EV;if("PerformanceObserver"in window&&"function"==typeof window.PerformanceObserver){a=new PerformanceObserver(r),f=new PerformanceObserver(i);try{a.observe({entryTypes:["paint"]}),f.observe({entryTypes:["largest-contentful-paint"]})}catch(p){}}if("addEventListener"in document){var l=!1,d=["click","keydown","mousedown","pointerdown","touchstart"];d.forEach(function(e){document.addEventListener(e,o,!1)})}}},{}],3:[function(e,n,t){function r(e,n){if(!i)return!1;if(e!==i)return!1;if(!n)return!0;if(!o)return!1;for(var t=o.split("."),r=n.split("."),a=0;a<r.length;a++)if(r[a]!==t[a])return!1;return!0}var i=null,o=null,a=/Version\/(\S+)\s+Safari/;if(navigator.userAgent){var f=navigator.userAgent,c=f.match(a);c&&f.indexOf("Chrome")===-1&&f.indexOf("Chromium")===-1&&(i="Safari",o=c[1])}n.exports={agent:i,version:o,match:r}},{}],4:[function(e,n,t){function r(e,n){var t=[],r="",o=0;for(r in e)i.call(e,r)&&(t[o]=n(r,e[r]),o+=1);return t}var i=Object.prototype.hasOwnProperty;n.exports=r},{}],5:[function(e,n,t){function r(e,n,t){n||(n=0),"undefined"==typeof t&&(t=e?e.length:0);for(var r=-1,i=t-n||0,o=Array(i<0?0:i);++r<i;)o[r]=e[n+r];return o}n.exports=r},{}],6:[function(e,n,t){n.exports={exists:"undefined"!=typeof window.performance&&window.performance.timing&&"undefined"!=typeof window.performance.timing.navigationStart}},{}],ee:[function(e,n,t){function r(){}function i(e){function n(e){return e&&e instanceof r?e:e?c(e,f,o):o()}function t(t,r,i,o){if(!l.aborted||o){e&&e(t,r,i);for(var a=n(i),f=v(t),c=f.length,u=0;u<c;u++)f[u].apply(a,r);var p=s[y[t]];return p&&p.push([b,t,r,a]),a}}function d(e,n){h[e]=v(e).concat(n)}function m(e,n){var t=h[e];if(t)for(var r=0;r<t.length;r++)t[r]===n&&t.splice(r,1)}function v(e){return h[e]||[]}function g(e){return p[e]=p[e]||i(t)}function w(e,n){u(e,function(e,t){n=n||"feature",y[t]=n,n in s||(s[n]=[])})}var h={},y={},b={on:d,addEventListener:d,removeEventListener:m,emit:t,get:g,listeners:v,context:n,buffer:w,abort:a,aborted:!1};return b}function o(){return new r}function a(){(s.api||s.feature)&&(l.aborted=!0,s=l.backlog={})}var f="nr@context",c=e("gos"),u=e(4),s={},p={},l=n.exports=i();l.backlog=s},{}],gos:[function(e,n,t){function r(e,n,t){if(i.call(e,n))return e[n];var r=t();if(Object.defineProperty&&Object.keys)try{return Object.defineProperty(e,n,{value:r,writable:!0,enumerable:!1}),r}catch(o){}return e[n]=r,r}var i=Object.prototype.hasOwnProperty;n.exports=r},{}],handle:[function(e,n,t){function r(e,n,t,r){i.buffer([e],r),i.emit(e,n,t)}var i=e("ee").get("handle");n.exports=r,r.ee=i},{}],id:[function(e,n,t){function r(e){var n=typeof e;return!e||"object"!==n&&"function"!==n?-1:e===window?0:a(e,o,function(){return i++})}var i=1,o="nr@id",a=e("gos");n.exports=r},{}],loader:[function(e,n,t){function r(){if(!x++){var e=E.info=NREUM.info,n=d.getElementsByTagName("script")[0];if(setTimeout(s.abort,3e4),!(e&&e.licenseKey&&e.applicationID&&n))return s.abort();u(y,function(n,t){e[n]||(e[n]=t)}),c("mark",["onload",a()+E.offset],null,"api");var t=d.createElement("script");t.src="https://"+e.agent,n.parentNode.insertBefore(t,n)}}function i(){"complete"===d.readyState&&o()}function o(){c("mark",["domContent",a()+E.offset],null,"api")}function a(){return O.exists&&performance.now?Math.round(performance.now()):(f=Math.max((new Date).getTime(),f))-E.offset}var f=(new Date).getTime(),c=e("handle"),u=e(4),s=e("ee"),p=e(3),l=window,d=l.document,m="addEventListener",v="attachEvent",g=l.XMLHttpRequest,w=g&&g.prototype;NREUM.o={ST:setTimeout,SI:l.setImmediate,CT:clearTimeout,XHR:g,REQ:l.Request,EV:l.Event,PR:l.Promise,MO:l.MutationObserver};var h=""+location,y={beacon:"bam.nr-data.net",errorBeacon:"bam.nr-data.net",agent:"js-agent.newrelic.com/nr-1167.min.js"},b=g&&w&&w[m]&&!/CriOS/.test(navigator.userAgent),E=n.exports={offset:f,now:a,origin:h,features:{},xhrWrappable:b,userAgent:p};e(1),e(2),d[m]?(d[m]("DOMContentLoaded",o,!1),l[m]("load",r,!1)):(d[v]("onreadystatechange",i),l[v]("onload",r)),c("mark",["firstbyte",f],null,"api");var x=0,O=e(6)},{}],"wrap-function":[function(e,n,t){function r(e){return!(e&&e instanceof Function&&e.apply&&!e[a])}var i=e("ee"),o=e(5),a="nr@original",f=Object.prototype.hasOwnProperty,c=!1;n.exports=function(e,n){function t(e,n,t,i){function nrWrapper(){var r,a,f,c;try{a=this,r=o(arguments),f="function"==typeof t?t(r,a):t||{}}catch(u){l([u,"",[r,a,i],f])}s(n+"start",[r,a,i],f);try{return c=e.apply(a,r)}catch(p){throw s(n+"err",[r,a,p],f),p}finally{s(n+"end",[r,a,c],f)}}return r(e)?e:(n||(n=""),nrWrapper[a]=e,p(e,nrWrapper),nrWrapper)}function u(e,n,i,o){i||(i="");var a,f,c,u="-"===i.charAt(0);for(c=0;c<n.length;c++)f=n[c],a=e[f],r(a)||(e[f]=t(a,u?f+i:i,o,f))}function s(t,r,i){if(!c||n){var o=c;c=!0;try{e.emit(t,r,i,n)}catch(a){l([a,t,r,i])}c=o}}function p(e,n){if(Object.defineProperty&&Object.keys)try{var t=Object.keys(e);return t.forEach(function(t){Object.defineProperty(n,t,{get:function(){return e[t]},set:function(n){return e[t]=n,n}})}),n}catch(r){l([r])}for(var i in e)f.call(e,i)&&(n[i]=e[i]);return n}function l(n){try{e.emit("internal-error",n)}catch(t){}}return e||(e=i),t.inPlace=u,t.flag=a,t}},{}]},{},["loader"]);</script><meta content="width=device-width, initial-scale=1" name="viewport" /><script type='text/javascript'>window.mobileRedirect = { mobileEnabled: 0, deepLinkUrl: '/m/#deepLink/%7b%22view%22%3a%22PressReleaseList%22%2c%22languageId%22%3a%221%22%7d'}</script>
    <script type="text/javascript" src="/js/mobileRedirect.js">
    </script>
    
    <!--[if lte IE 8]>
<link id="respond-proxy" rel="respond-proxy" media="screen" href="//barrick.q4cdn.com/788666289/files/js/respond-proxy.html" />
<link id="respond-redirect" rel="respond-redirect" media="screen" href="https://www.barrick.com/js/respond.proxy.gif" />
<![endif]-->

<link type="text/css" rel="stylesheet" media="all" href="//fonts.googleapis.com/css?family=Open+Sans:400,300,600,700" />
<link type="image/x-icon" rel="icon" media="" href="//barrick.q4cdn.com/788666289/files/favicon.ico" />
<link type="image/x-icon" rel="shortcut icon" media="" href="//barrick.q4cdn.com/788666289/files/favicon.ico" />
<link rel="stylesheet" media="print" href="//barrick.q4cdn.com/788666289/files/css/print.css" />
<link type="text/css" rel="stylesheet" media="all" href="//barrick.q4cdn.com/788666289/files/css/select2.min.css" />
<link id="htmlGlobalLinkCss" type="text/css" rel="stylesheet" media="all" href="//barrick.q4cdn.com/788666289/files/css/global.css?v=85318" /><link id="htmlClientLinkCss" type="text/css" rel="stylesheet" media="all" href="//barrick.q4cdn.com/788666289/files/css/client.css?v=84923" /><link id="htmlLinkPrintCss" type="text/css" rel="stylesheet" media="print" href="//barrick.q4cdn.com/788666289/files/css/print.css" /><script type="text/javascript" src="//barrick.q4cdn.com/788666289/files/js/q4.core.1.0.0.min.js"></script>
<script type="text/javascript" src="//barrick.q4cdn.com/788666289/files/js/q4.app.1.0.1.min.js"></script>
<script type="text/javascript" src="//barrick.q4cdn.com/788666289/files/js/q4.api.js"></script>
<script type="text/javascript" src="//widgets.q4app.com/widgets/requireslib/moment.min.js"></script>
<script type="text/javascript" src="//barrick.q4cdn.com/788666289/files/js/select2.min.js"></script>
<script type="text/javascript" src="//barrick.q4cdn.com/788666289/files/js/in-view.min.js"></script>
<script type="text/javascript" src="//barrick.q4cdn.com/788666289/files/js/jquery.hoverdir.js"></script>
<!--[if lte IE 8]>
<script type="text/javascript" src="https://www.barrick.com/js/respond.proxy.js"></script>
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

    var trackingCodes = [{qualifier: 'Q4', trackingCode: 'UA-26185251-1'}];
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
    
    
    <div id="pageClass" class="Sectionhome PageDefault PageNews LayoutThreeColumnLayout Languageen-US -News section--news-theme">
        <div class="PageDefaultInner">
            <div id="litPageDiv" class="PageNews SectionNews ParentSection_home">
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
                    
<div class="layout layout--three-column">
    <div class="layout_inner">
        <div class="layout_header">
            <div class="pane pane--header">
                <div class="pane_inner clearfix">
                    <span class='HeaderPaneDiv'><span class='HeaderPaneDiv1'><div id="_ctrl0_ctl06_divModuleContainer" class="module module-embed module-skip">
    <div class="module_container module_container--outer">
        
        <div class="module_container module_container--inner">
            <script type="text/javascript">var whoistrack_params=whoistrack_params||[];whoistrack_params.push(["wait","e1c8c65007f84ac59b79222dbdd48588"]);var t=document["createElement"]("script"),i;t["type"]="text/javascript";t["src"]=window["location"]["href"]["split"]("/")[0]+"//app.whoisvisiting.com/who.js";i=document["getElementsByTagName"]("script")[0];i["parentNode"]["insertBefore"](t,i);</script>
<a class="module-skip_link" href="#maincontent">Skip to main content</a>
        </div>
    </div>
</div></span><span class='HeaderPaneDiv2'><div id="_ctrl0_ctl09_divModuleContainer" class="module module-embed hidden">
    <div class="module_container module_container--outer">
        
        <div class="module_container module_container--inner">
            <script type="text/javascript" src="//barrick.q4cdn.com/788666289/files/js/jarallax.min.js"></script>
<script type="text/javascript" src="//barrick.q4cdn.com/788666289/files/js/jarallax-element.min.js"></script>
<script>

var q4App = $.extend(true, q4Defaults, {
    cookie: {
        setCookie: function(cname, cvalue, exdays) {
            var d = new Date();
            d.setTime(d.getTime() + (exdays*24*60*60*1000));
            var expires = "expires="+ d.toUTCString();
            if(exdays>0){
                document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
            }else{
                document.cookie = cname + "=" + cvalue + ";path=/";
            }
        },
        getCookie: function(cname) {
            var name = cname + "=";
            var ca = document.cookie.split(';');
            for(var i = 0; i <ca.length; i++) {
                var c = ca[i];
                while (c.charAt(0)==' ') {
                    c = c.substring(1);
                }
                if (c.indexOf(name) == 0) {
                    return c.substring(name.length,c.length);
                }
            }
            return "";
        } 
    },
    siteSettings: {
        setContrast: function(layout, trigger){
            if (q4App.cookie.getCookie("barrickcontrast") == "high"){
                $(layout).addClass('js--high-contrast');
                $(trigger).addClass('js--active');
            }else{
                $(layout).removeClass('js--high-contrast');
                $(trigger).removeClass('js--active');
            }
            $(trigger).click(function(e){
                $(this).toggleClass('js--active');
                if($(this).hasClass('js--active')){
                    $(layout).addClass('js--high-contrast');
                    q4App.cookie.setCookie("barrickcontrast", "high", 365);
                }else{
                    $(layout).removeClass('js--high-contrast');
                    q4App.cookie.setCookie("barrickcontrast", "normal", 365);
                }
                
            });
        }
    },
    menuTheme: function(navClass){
        var menuThemePatterns = [{
                contains: "Operations", themeClass: 'js--operations-theme'
            },{
                contains: "Sustainability", themeClass: 'js--sustainability-theme'
            },{
                contains: "News", themeClass: 'js--news-theme'
            },{
                contains: "Careers", themeClass: 'js--careers-theme'
            },{
                contains: "Investors", themeClass: 'js--investors-theme'
            },{
                contains: "About", themeClass: 'js--about-theme'
            }];
        $(navClass).find('.level1 > li > a').each(function(){
            var link = $(this);
            menuThemePatterns.forEach(function(pattern, i, arr){
                if(link.text().indexOf(pattern.contains) > -1){
                    link.parent().addClass(pattern.themeClass);
                }
            });
        });
    },
    menu: function(){
        var columnLinks = $('.nav--main .js--operations-theme .level2 > li');
        for(var i = 0; i < columnLinks.length; i+=4) {
            columnLinks.slice(i, i+4).wrapAll("<li class='has-children'></li>");
        }
        var columnLinks2 = $('.nav--mobile .js--operations-theme .level2 > li');
        for(var i = 0; i < columnLinks2.length; i+=4) {
            columnLinks2.slice(i, i+4).wrapAll("<li class='has-children'></li>");
        }
        $('.nav--main .level1 > li, .nav--mobile .level1 > li').each(function(){
            if( $(this).find('.level2 > li').hasClass('has-children') ) {
                $(this).find('.level2').addClass('js--has-children');
            }
        });
        $('.nav--mobile ul.level1 > li.has-children > a').on('click', function(e){
            var $this = $(this),
                $parent = $this.parent();
            if (!$parent.hasClass('js--expanded')) {
                e.preventDefault();
                $parent.addClass('js--expanded').siblings('.js--expanded').removeClass('js--expanded');
                $('.layout').addClass('js--nav-expanded');
            }
        });
        if(this.isMobile.any()){
            $('.nav--main .has-children > a').click(function(e){
                if(!$(this).hasClass('js--prevented-once')){
                    e.preventDefault();
                    $(this).addClass('js--prevented-once').parent().siblings().find('.js--prevented-once').removeClass('js--prevented-once');
                }
            });
        }
        $('.nav--main .level1 > li.has-children').hover(function() {
            $(this).addClass('js--hover');
            $('.layout_header').addClass('js--menu-open');
        }, function(){
            $(this).removeClass('js--hover');
            $('.layout_header').removeClass('js--menu-open');
        });
    },
    langSwitch: function(){
        $('.module-language_title').on('click', function(){
            $(this).parent().toggleClass('js--active');
        });
    },
    search: function(){
        $('.pane--header .module-search .module_title').on('click', function(){
            $(this).parent().toggleClass('js--active');
            $(this).next().find('input').trigger('focus');
        });
        $('input.addsearch').on('keydown',function(e) { 
            if(e.keyCode === 13) { 
                event.preventDefault(); 
                window.location = '/search-results/default.aspx?term=' + $(this).val().replace(/ /g, '\+');
            } 
        });
    },
    mobileMenuToggle: function($layout, pane, toggle) {
        var inst = this;
        $layout.on('click', toggle, function(e) {
            $layout.toggleClass('js--mobile');
            if($layout.hasClass('js--mobile')){
                $('.module-language .js--active').removeClass('js--active');
            }else{
                $('.nav--mobile .js--expanded').removeClass('js--expanded');
            }
            // inst._onMobileMenuExpand($('.js--mobile ' + pane + ' .nav'));
        });
    },
    select2: function(selector){
        $.each(selector,function(){
            var _ = $(this);

            if(_.data('placeholder') != undefined){
                _.val('').select2({
                    placeholder: _.data('placeholder'),
                    minimumResultsForSearch : -1
                }); 
            } else {
                _.select2({
                    minimumResultsForSearch : -1
                });
            }

            $(window).on('scroll', function(){
                _.select2('close');
                if( $('.select2-container--default').hasClass('select2-container--focus') ){
                    $('.select2-container--default').removeClass('select2-container--focus');
                }
            });
        });
    },
    parallax: function($selector){
        $selector.jarallax({
            speed: ((-1/14)*$(window).height()).toString(),
            type: 'element'
        });
        $selector.addClass('js--parallax');
    },
    inViewport: function(elemClass, offset){
        $.fn.isInViewport = function(offset) {
            var elementTop = $(this).offset().top;
            var elementBottom = elementTop + $(this).outerHeight();
            var viewportTop = $(window).scrollTop();
            var viewportBottom = viewportTop + $(window).height();
            return elementBottom + $(this).outerHeight() * offset > viewportTop && elementTop + $(this).outerHeight() * offset < viewportBottom;
        };
        $(window).on('scroll.inViewport', function(){
            $.each($(elemClass), function(i, elem){
                if($(elem).isInViewport(offset)){
                    if(!$(elem).hasClass('js--inviewport')){
                        $(elem).addClass('js--inviewport');
                        $(elem).find('.check-viewport-animate-this').not('.animation--js-delayed').addClass('js--animate');
                        if ($(elem).find('.animation--js-delayed').length){
                            $.each($(elem).find('.animation--js-delayed'), function(j, delayedElem){
                                setTimeout(function(){
                                    $(delayedElem).addClass('js--animate');
                                },300*j);
                            });
                        }
                        
                    }
                    
                }else{
                    if($(elem).hasClass('js--inviewport')){
                        $(elem).removeClass('js--inviewport');
                        $(elem).find('.check-viewport-animate-this').removeClass('js--animate');
                    }
                    
                }
            });
            
        });
        
    },
    headerScroll: function(){
        var $this = $('.pane--header');
        var mainStoryBottom;
        var lastScrollPos = 0;
        var canBeShrinked = true;
        var faded = false;
        $(window).on('scroll.scrollheader', function(){
            scrollPos = $(window).scrollTop();

            
            if(scrollPos > mainStoryBottom){
                    if(scrollPos > lastScrollPos){
                        if (!faded){
                            $this.addClass('js--scrollheader-fade').css({'margin-top': -$this.outerHeight()});
                            $('.module-back-to-top').addClass('js--active');
                            canBeShrinked = false;
                            faded = true;
                            $('.layout_header').removeClass('js--menu-open');
                        }
                    }else{
                        if (faded){
                            $this.removeClass('js--scrollheader-fade').addClass('js--scrollheader-shrink').css({'margin-top': 0});
                            $('.module-back-to-top').removeClass('js--active');
                            canBeShrinked = true;
                            faded = false;
                        }
                    }
                    if(canBeShrinked){
                       $this.addClass('js--scrollheader-shrink'); 
                    }
                
            }else{
                if (scrollPos <= lastScrollPos){
                    // console.log('scrollUp');
                    if(canBeShrinked){
                       $this.removeClass('js--scrollheader-shrink'); 
                    }
                    

                }else{
                    // console.log('scrollDown');
                    if(canBeShrinked){
                        $this.addClass('js--scrollheader-shrink');
                    }
                }
                if (faded){
                    $this.removeClass('js--scrollheader-fade').css({'margin-top': 0});
                    $('.module-back-to-top').removeClass('js--active');
                    canBeShrinked = true;
                    faded = false;
                }

            }
            lastScrollPos = $(window).scrollTop();
        });
        $(window).on('resize.scrollheader', function(){
            mainStoryBottom = $('.pane--banner').offset().top + $('.pane--banner').outerHeight();
        }).trigger('resize.scrollheader');
    },
    fixPostHeader: function(postHeader, mainStory){
        if($(postHeader).length == 1){
            var $this = $(postHeader);
            var mainStoryBottom = $(mainStory).offset().top + $(mainStory).outerHeight();
            var isFixed = false;
            var elPlaceholder = $('<div />').addClass('js--post-header-placeholder'+' '+$(postHeader)[0].className).css({'height':$this.outerHeight()});
            $(window).on('scroll.scollHeader', function(){
                scrollPos = $(window).scrollTop();
                if(mainStoryBottom < scrollPos){
                    if(!isFixed){
                        $this.after(elPlaceholder);
                        $this.addClass('js--post-header-fixed');
                        isFixed = true;
                    }
                    
                }else{
                    if(isFixed)
                    elPlaceholder.remove();
                    $this.removeClass('js--post-header-fixed').removeAttr('style');
                    isFixed = false;
                }
            });
            $(window).on('resize.scollHeader', function(){
                mainStoryBottom = $(mainStory).offset().top + $(mainStory).outerHeight();
                elPlaceholder.css({'height':$this.outerHeight()});
            });
        }
            
    },
    tooltip: function(){
        $(window).on('resize.tooltip', function(){
            $('.tooltip').each(function(i, item){
                var $trigger = $(item).find('.tooltip_btn');
                var $box = $(item).find('.tooltip_info');
                var triggerPos = {
                    top: $trigger.offset().top,
                    left: $trigger.offset().left,
                    bottom: $trigger.offset().top + $trigger.outerHeight(),
                    right: $trigger.offset().left + $trigger.outerWidth()
                };
                var boxPos = {
                    top:'100%',
                    bottom: 'auto',
                    left: '100%',
                    right: 'auto'
                };

                if (triggerPos.top - $box.outerHeight() < 0){
                    boxPos.top = '100%';
                    boxPos.bottom = 'auto';
                }
                if (triggerPos.bottom + $box.outerHeight() > $(document).height()){
                    boxPos.top = 'auto';
                    boxPos.bottom = '100%';
                }
                if (triggerPos.left - $box.outerWidth() < 0){
                    boxPos.left = '100%';
                    boxPos.right = 'auto';
                }
                if (triggerPos.right + $box.outerWidth() > $(window).width()){

                    boxPos.left = 'auto';
                    boxPos.right = '100%';
                }

                $box.css(boxPos);
            });
        }).trigger('resize.tooltip');
        
    },
    ytVideoBanner: {
        ytInst: null,

        init: function(options){
            var defaults = {
                containerId: '',
                $containerToFill: '',
                ytVideoId: ''
            }
            var o = $.extend(true, defaults, options);
            
            var inst = this;

            window.onYouTubeIframeAPIReady = function() {
                inst.ytInst = new YT.Player(o.containerId, {
                  videoId: o.ytVideoId,
                  events: {
                    'onReady': onPlayerReady,
                    'onStateChange': onPlayerStateChange
                  },
                  playerVars: {autoplay: 1, autohide: 1, modestbranding: 0, rel: 0, showinfo: 0, controls: 0, disablekb: 1, enablejsapi: 0, iv_load_policy: 3}
                });
            }
            function onPlayerReady(event) {
                event.target.playVideo();
                event.target.mute();
                vidRescale();
            }
            function onPlayerStateChange(event) {
                if (event.data === 1){
                    vidRescale();
                    $('#'+o.containerId).addClass('js--active');

                } else if (event.data === 0){
                    event.target.playVideo();
                    event.target.mute();
                }
            }

            function vidRescale(){
                if(inst.ytInst !== null){
                    var w = o.$containerToFill.outerWidth(),
                        h = o.$containerToFill.outerHeight();

                    if (w/h > 16/9){
                        inst.ytInst.setSize(w, w/16*9);
                        $('#'+o.containerId).css({
                            'top': -($('#'+o.containerId).outerHeight()-h)/2,
                            'left': '0px',
                            'width': w,
                            'height': w/16*9
                        });
                    } else {
                        inst.ytInst.setSize(h/9*16, h);
                        $('#'+o.containerId).css({
                            'top':'0px',
                            'left': -($('#'+o.containerId).outerWidth()-w)/2,
                            'width': h/9*16,
                            'height': h
                        });
                    }
                }
                
            }
            $(window).on('resize.vidRescale', function(){
              vidRescale();
            });

            var tag = document.createElement('script');
                tag.src = 'https://www.youtube.com/iframe_api';
            var firstScriptTag = document.getElementsByTagName('script')[0];
                firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

        }
    },
    backToTop: function(){
        $('.module-back-to-top').on('click', function(){
            $('html, body').animate({scrollTop: 0});
        });
    },
    accessibleNav: function($nav, topLevel) {
        $nav.on('focus ', 'a' ,function(e) {
            var $link = $(this);
            $link.closest('ul').find('li').removeClass('js--focused');
            $link.closest('li').addClass('js--focused');
            if ( 
                ($link.closest('li').is(':last-child') && !$link.closest('li').hasClass('has-children') && $link.closest('ul').is(topLevel)) ||
                ($link.closest('li').is(':last-child') && $link.closest('li').closest('ul').closest('li').is(':last-child') && $link.closest('ul').parent('li').closest('ul').is(topLevel))
            ){
                $link.blur(function() {
                    $link.closest(topLevel).find('li').removeClass('js--focused');
                });
            }
        });
        $('body').on('click', function(e){
            if (!$nav.is(e.target) // if the target of the click isn't the container...
                && $nav.has(e.target).length === 0) // ... nor a descendant of the container
            {
                $nav.find('.js--focused').removeClass("js--focused");
            }   
        });
    },
    addToAny: function(){
        var tag = document.createElement('script');
            tag.src = 'https://static.addtoany.com/menu/page.js';
        var firstScriptTag = document.getElementsByTagName('script')[0];
            firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

        $('.module-add-to-any_trigger').on('click', function(e){
            e.preventDefault();
            $(this).toggleClass('js--active').next().toggleClass('js--active');
        });

        $(document).mousedown(function (e){
            if (!$('.module-add-to-any').is(e.target)
                && $('.module-add-to-any').has(e.target).length === 0){
                $('.module-add-to-any .js--active').removeClass('js--active');
            }
        });
    },
    video: function(){
        $(".module-video_play").click(function(){
            $.fancybox.open({
                src : $(this).data('src')
            });
        });
    },
    reveal: function(container, trigger, panel, once) {
        $(trigger).attr('tabindex', '0');
        $(panel).attr('aria-hidden', 'true');
        if (once) {
            $(container).one('click keypress', trigger, function(e) {
                if (e.keyCode == 13 || e.type == 'click') {
                    if ($(this).is('a')) e.preventDefault();
                    $(this).toggleClass('js--active').closest(container).find(panel).slideToggle();
                    $(panel).attr('aria-hidden', function(i, attr) {
                        return attr == 'true' ? 'false' : 'true';
                    });
                }
            });
        } else {
            $(container).on('click keypress', trigger, function(e) {
                if (e.keyCode == 13 || e.type == 'click') {
                    if ($(this).is('a')) e.preventDefault();
                    $(this).toggleClass('js--active').closest(container).find(panel).slideToggle();
                    $(panel).attr('aria-hidden', function(i, attr) {
                        return attr == 'true' ? 'false' : 'true';
                    });
                }
            });
        }
    },
    downloadsModuleSelect: function(selector){
        var inst = this;
        var itemData = [];
        var timestamp = (new Date()).getTime(); //for generating unique IDs for selects

        $.each($(selector), function(i, dl){
            var $dl = $(dl);
            $.each($dl.find('.module_item .module-downloads_title'), function(j, title){
                var $title = $(title);
                itemData.push({
                    title: $title.text(),
                    index: j
                });
            });

            $dl.find('.module_container--content').prepend(Mustache.render(
                    '<div class="module_options">' +
                        '<label class="module_options-label sr-only" for="Documents-'+timestamp+'">Select:</label>' +
                        '<select style="width:320px;" data-placeholder="Select Documents" class="module_options-select" id="Documents-'+timestamp+'">' +
                            '{{#.}}' +
                                '<option value="{{index}}">{{title}}</option>' +
                            '{{/.}}' +
                        '</select>' +
                    '</div>', 
                    itemData))
                .find('.module_item').addClass('js--hidden');

            $dl.find('select').on('change', function(se){
                $dl.find('.module_item').eq($(this).find('option:selected').val()).removeClass('js--hidden').siblings('.module_item').addClass('js--hidden');
            });
            inst.select2($dl.find('select'));
        });
    },
    heightsNormalizer: function(){
        this.setHeights = function(args){
            
            var applyOnResize = function(func){
                var timer=false;
                function hnresizeCallback(){
                    clearTimeout(timer);
                    timer = setTimeout(func, args.resizeDelay);
                }
                hnresizeCallback();
                $(window).resize(function(){
                    hnresizeCallback();
                });
            }
            
            var perRow, 
                elements = args.elemSelector; //define cells object
            if (args.responsive != null && args.responsive.length>0){
                //if there are any breakpoints set, search for the right one to get cells per row
                applyOnResize(function(){
                    var wwidth = $(window).width();
                    for(a = args.responsive.length-1; a >= 0; a--){

                        if (args.responsive[a].breakpoint>=wwidth){
                            perRow = args.responsive[a].perRow;
                            return false;
                        }else{
                            if(args.responsive[a-1] == undefined){
                                perRow = args.perRow;
                                return false;
                            }
                        }
                    }
                });
            }else{
                //else use global "cells per row" value
                perRow = args.perRow;
            }
            var main = function(){
                elements.css('height', 'auto');
                //if cells are not standing side by side, do not apply any style and exit function
                if (perRow == 1){
                    return false;
                }
                for (i = 0; i<elements.length; i += perRow ){ //iterate throughout each row

                    this.maxRowHeight = 0;
                    for (var j = i; j < i+perRow; j++){ //iterate throughout each cell of the row in search for the highest cell
                        if(elements.eq(j).height() > this.maxRowHeight){
                            this.maxRowHeight = elements.eq(j).height();
                        }
                    }
                    for (var k = i; k < i+perRow; k++){ //iterate throughout each cell of the row to set the updated height
                        elements.eq(k).height(this.maxRowHeight);
                    }
                }
            }
            this.mainAction = main;
            if (args.updateOnResize){
                applyOnResize(function(){
                    main();
                });
            }
        }
    },
    appendAnimatedIcons: function(elemsArray$){
        $.each(elemsArray$, function(i, $item){
            if(!$item.find('.button_animated-icon').length){
                $item.append(
                    '<span class="button_animated-icon js--appended">'+
                        '<span class="button_animated-icon_line"></span>'+
                        '<span class="button_animated-icon_bullet--inflatable"></span>'+
                    '</span>'
                );
            }    
        });
    },
    linkToSection: function(){
        $('.nav--main .level2 a[href*="section="], .nav--mobile .level2 a[href*="section="]').on('click', function(e) {
            var sectionLinkArr = [];
            if($('.section-link').length) {
                $('.section-link').each(function() {
                    sectionLinkArr.push($(this).attr('name'));
                });
                var linkHref = $(this).attr('href').split('#section=');
                if(sectionLinkArr.indexOf(linkHref[1]) > -1) {
                    e.preventDefault();
                    $('html,body').animate({
                        scrollTop: $('[name="'+linkHref[1]+'"]').offset().top - 80
                    });
                }
            }
        });
    },
    downloadListColumns: function(){
        setHeight = new q4App.heightsNormalizer();
        setHeight.setHeights({
            elemSelector: $('.module-downloads--columns .module-downloads_title'),
            perRow: 4,
            updateOnResize: true,
            resizeDelay: 150,
            responsive: [
                //breakpoints must be in correct reverse order to work properly (ex: 1024 > 768 > 480)
                {
                    breakpoint:767,
                    //to not apply any style, set perRow = 1
                    perRow: 3
                },{
                    breakpoint:479,
                    //to not apply any style, set perRow = 1
                    perRow: 2
                }
            ]
        });
    },
    init: function() {
        var app = this;
        app.appendAnimatedIcons([$('.button--go'), $('.button--linkout'), $('.button--download'), $('.button--loadmore'), $('.module_view-all-link')]);
        app.downloadsModuleSelect('.module-downloads--select');
        app.addToAny();
        app.backToTop();
        app.headerScroll();
        app.fixPostHeader('.module-page-title-post--fixed', '.pane--banner');
        app.inViewport('.check-viewport', 0.6);
        app.parallax($('.floating').not('.js--parallax'));
        app.cleanUp();
        app.unWrapLink('a.module-stock-header_stock-price');
        app.submitOnEnter('.module-unsubscribe');
        app.mobileMenuToggle($('.layout'), '.pane--navigation', '.layout_toggle i');
        app.cleanQuickLinks($('.module-links'));
        app.copyright($('.copyright_year'))
        app.reveal('.module_read-more-container', '.module_read-more-trigger', '.module_read-more-panel', false);
        app.docTracking();
        app.fancySignup();
        app.resetDate(['.nav a[href*="s3.q4web.com"]:not([href$=".pdf"])']);
        app.previewToolbar();
        app.siteSettings.setContrast('.layout', '.module-contrast_toggle');
        app.menuTheme('.nav--main, .nav--mobile');
        app.menu();
        app.accessibleNav($('.nav--main'), '.level1');
        // app.androidTap($('.nav--main'));
        app.langSwitch();
        app.search();
        app.select2($('select'));
        app.tooltip();
        app.video();
        app.linkToSection();
        app.downloadListColumns();
    }
});

$(function (){
    q4App.init();
    if ( $('.accordion').hasClass('accordion--closed') ){
        q4App.toggle(
            $('.accordion'), // Containing Element
            '.accordion_item', // Item Selector
            '.accordion_trigger', // Toggle Selector
            '.accordion_panel', // Panel Selector
            false, // Accordion functionality?
            false, // Show all / Hide all button?
            false); // Open first item?
    } else {
        q4App.toggle(
            $('.accordion'), // Containing Element
            '.accordion_item', // Item Selector
            '.accordion_trigger', // Toggle Selector
            '.accordion_panel', // Panel Selector
            false, // Accordion functionality?
            false, // Show all / Hide all button?
            false); // Open first item?
    }
});

$(window).on('load', function(){
    var sectionLinkArr = [];
    if($('.section-link').length) {
        $('.section-link').each(function() {
            sectionLinkArr.push($(this).attr('name'));
        });
        var linkHref = window.location.href.split('#section=');
        if(sectionLinkArr.indexOf(linkHref[1]) > -1) {
            $('html,body').animate({
                scrollTop: $('[name="'+linkHref[1]+'"]').offset().top - 80
            });
        }
    }

    $('.map--controls_slider .map--controls_slider--btn').on('click', function(e) {
        e.preventDefault(); // prevent button from reloading page
    });
});

</script>
        </div>
    </div>
</div></span><span class='HeaderPaneDiv3'><div id="_ctrl0_ctl12_divModuleContainer" class="module module-embed">
    <div class="module_container module_container--outer">
        
        <div class="module_container module_container--inner">
            <script type="text/javascript">
    var newstags = {

        topics: [
            { tag: 'innovation',   label: 'Innovation' },
            { tag: 'investors',    label: 'Press Release' },
            { tag: 'environment',  label: 'Environment' },
            { tag: 'communities',  label: 'Communities' },
            { tag: 'education',    label: 'Education' },
            { tag: 'partnership',  label: 'Partnership' },
            { tag: 'performance',  label: 'Performance' },
            { tag: 'perspectives', label: 'Perspectives' },
            { tag: 'profile',      label: 'Profile' },
            { tag: 'mining',       label: 'Mining' }
        ],

        topicDefault: { tag: '', label: 'News' },

        trimSentence: function(text, textTength){
            if ( text.length > textTength ) {
                text = text.substr(0, textTength);
                text = text.substr(0, Math.min(text.length, text.lastIndexOf(' ')))+'...';
                return text;
            } else {
                return text;
            }
        },

        addTopicsToItems: function(items){
            var inst = this;
            $.each(items, function(i, item) {
                item.topics = [];

                item.title = newstags.trimSentence(item.title, 87);

                $.each(item.tags, function(j, tag) {
                    $.each(inst.topics, function(k, topic) {
                        if (tag == topic.tag && item.topics.length == 0 ) {
                            item.topics.push({label: topic.label, tag: topic.tag});
                        }
                    });
                });

                if (item.topics.length == 0){
                    item.topics.push({label: inst.topicDefault.label, tag: inst.topicDefault.tag});
                }
            });
        }
    }; 
</script>
        </div>
    </div>
</div></span><span class='HeaderPaneDiv4'><div id="_ctrl0_ctl15_divModuleContainer" class="module module-embed module-logo">
    <div class="module_container module_container--outer">
        
        <div class="module_container module_container--inner">
            <a href="/home/default.aspx">
    <img src="//barrick.q4cdn.com/788666289/files/design/svg/BARRICK-GOLD-logo.svg" alt="Barrick Logo" />	
</a>
        </div>
    </div>
</div></span><span class='HeaderPaneDiv5'><nav class="nav nav--main"><ul class="level1">
	<li class="has-children"><a href="https://www.barrick.com/English/about/default.aspx">About</a><ul class="level2">
		<li><a href="https://www.barrick.com/English/about/management/default.aspx">Management</a></li><li><a href="https://www.barrick.com/English/about/governance/default.aspx">Governance & Board of Directors</a></li><li><a href="https://www.barrick.com/English/contact-us/default.aspx">Contact Us</a></li>
	</ul></li><li class="has-children"><a href="https://www.barrick.com/English/operations/default.aspx">Operations</a><ul class="level2">
		<li><a href="https://www.barrick.com/English/operations/nevada-gold-mines/default.aspx">Nevada Gold Mines</a></li><li><a href="https://www.barrick.com/English/operations/Bulyanhulu/default.aspx">Bulyanhulu</a></li><li><a href="https://www.barrick.com/English/operations/Buzwagi/default.aspx">Buzwagi</a></li><li><a href="https://www.barrick.com/English/operations/hemlo/default.aspx">Hemlo</a></li><li><a href="https://www.barrick.com/English/operations/jabal-sayid/default.aspx">Jabal Sayid</a></li><li><a href="https://www.barrick.com/English/operations/kibali/default.aspx">Kibali</a></li><li><a href="https://www.barrick.com/English/operations/loulo-gounkoto/default.aspx">Loulo-Gounkoto</a></li><li><a href="https://www.barrick.com/English/operations/lumwana/default.aspx">Lumwana</a></li><li><a href="https://www.barrick.com/English/operations/North-Mara/default.aspx">North Mara</a></li><li><a href="https://www.barrick.com/English/operations/porgera/default.aspx">Porgera</a></li><li><a href="https://www.barrick.com/English/operations/pueblo-viejo/default.aspx">Pueblo Viejo</a></li><li><a href="https://www.barrick.com/English/operations/tongon/default.aspx">Tongon</a></li><li><a href="https://www.barrick.com/English/operations/veladero/default.aspx">Veladero</a></li><li><a href="https://www.barrick.com/English/operations/zaldivar/default.aspx">Zaldívar</a></li><li><a href="https://www.barrick.com/English/operations/exploration-and-projects/default.aspx">Exploration & Projects</a></li>
	</ul></li><li class="has-children"><a href="https://www.barrick.com/English/sustainability/default.aspx">Sustainability</a><ul class="level2">
		<li><a href="https://www.barrick.com/English/sustainability/our-approach/default.aspx">Our Approach</a></li><li><a href="https://www.barrick.com/English/sustainability/social-and-economic-development/default.aspx">Social & Economic Development</a></li><li><a href="https://www.barrick.com/English/sustainability/health-and-safety/default.aspx">Health & Safety</a></li><li><a href="https://www.barrick.com/English/sustainability/human-rights/default.aspx">Human Rights</a></li><li><a href="https://www.barrick.com/English/sustainability/environment/default.aspx">Environment</a></li><li><a href="https://www.barrick.com/sustainability/environment/default.aspx#tailings">Tailings Management</a></li><li><a href="https://www.barrick.com/English/sustainability/reports-policies/default.aspx">Reports & Policies</a></li>
	</ul></li><li class="has-children"><a href="https://www.barrick.com/English/investors/default.aspx">Investors</a><ul class="level2">
		<li><a href="https://www.barrick.com/English/investors/annual-report/default.aspx">Annual Report</a></li><li><a href="https://www.barrick.com/English/investors/agm/default.aspx">Annual Meeting</a></li><li><a href="https://www.barrick.com/English/investors/presentations-reports/default.aspx">Presentations & Reports</a></li><li><a href="/news/default.aspx#investors">Press Releases</a></li><li><a href="https://www.barrick.com/English/investors/shares-dividends/default.aspx">Shares & Dividends</a></li><li><a href="https://apps.indigotools.com/IR/IAC/?Ticker=GOLD&amp;Exchange=NYSE" target="_blank">Analyst Centre</a></li>
	</ul></li><li><a href="https://www.barrick.com/English/careers/default.aspx">Careers</a></li><li class="selected"><a href="https://www.barrick.com/English/news/default.aspx">News</a></li>
</ul></nav></span><span class='HeaderPaneDiv6'><div id="_ctrl0_ctl21_divModuleContainer" class="module module-embed layout_toggle circle-icon">
    <div class="module_container module_container--outer">
        
        <div class="module_container module_container--inner">
            <a href="#">
    <i class="q4-icon_hamburger" tabindex="0"></i>
    <span class="sr-only">Menu</span>
</a>
        </div>
    </div>
</div></span><span class='HeaderPaneDiv7'><div id="_ctrl0_ctl24_divContainer" class="module-language-switch">
    
            
            
        
            
            <a id="_ctrl0_ctl24_rtrLanguages_ctl01_lnkLanguage" href="https://www.barrick.com/Spanish/noticias/default.aspx" href="javascript:__doPostBack(&#39;_ctrl0$ctl24$rtrLanguages$ctl01$lnkLanguage&#39;,&#39;&#39;)">Spanish</a>
        
</div></span><span class='HeaderPaneDiv8'><div id="_ctrl0_ctl27_divModuleContainer" class="module module-html module-contrast circle-icon">
    <div class="module_container module_container--outer">
        
        <div class="module_container module_container--inner">
            <div class="module-contrast_toggle">
    <a>
        <i class="q4-icon_contrast"></i>
        <span class="sr-only">Set high contrast</span>
    </a>
</div>
        </div>
    </div>
</div></span><span class='HeaderPaneDiv9'><div id="_ctrl0_ctl30_divModuleContainer" class="module module-embed module-search circle-icon">
    <div class="module_container module_container--outer">
        <h2 id="_ctrl0_ctl30_lblTitle" class="module_title"><span id="_ctrl0_ctl30_lblModuleTitle" class="ModuleTitle"><a href="#"><i class="q4-icon_search"></i><span class="sr-only">Search Toggle</span></a></span></h2>
        <div class="module_container module_container--inner">
            <input type="text" class="addsearch" aria-label="Search query" placeholder="Search" />

<script type="text/javascript" src="https://addsearch.com/js/?key=c5403e8a4df4ddab045e4227fff2ad46"></script>
        </div>
    </div>
</div></span></span>
                </div>
            </div>
            <div class="pane pane--breadcrumb">
                <span class='BreadcrumbPaneDiv12'><div id="_ctrl0_ctl36_divModuleContainer" class="module module-embed module-stock-header dark">
    <div class="module_container module_container--outer">
        
        <div class="module_container module_container--inner">
            <div class="module_container module_container--container">
    <span class="gold"></span>
    <span class="tsx"></span>
    <span class="nyse"></span>
</div>

<script type="text/javascript" src="//widgets.q4app.com/widgets/q4.stockQuote.1.0.7.min.js"></script>
<script type="text/javascript">
    $('.module-stock-header .gold').stockQuote({
        loadingMessage: '',
        stock: ['USD:XAU'],
        stockTpl: (
            '{{#.}}' +
                '<a href="/investors/shares-dividends/default.aspx">' +
                    '<span class="module-stock-header_description1">GOLD:</span>' +
                    '<span class="module-stock-header_stock-price">${{tradePrice}}</span>' +
                '</a>' +
            '{{/.}}'
        )
    });
    $('.module-stock-header .tsx').stockQuote({
        loadingMessage: '',
        stock: ['TSE:ABX.CA'],
        stockTpl: (
            '{{#.}}' +
                '<a href="/investors/shares-dividends/default.aspx">' +
                    '<span class="module-stock-header_description1">ABX (TSX)</span>' +
                    '<span class="module-stock-header_stock-price">${{tradePrice}}</span>' +
                '</a>' +
            '{{/.}}'
        )
    });
    $('.module-stock-header .nyse').stockQuote({
        loadingMessage: '',
        stock: ['NYSE:GOLD.N'],
        stockTpl: (
            '{{#.}}' +
                '<a href="/investors/shares-dividends/default.aspx">' +
                    '<span class="module-stock-header_description1">GOLD (NYSE)</span>' +
                    '<span class="module-stock-header_stock-price">${{tradePrice}}</span>' +
                '</a>' +
            '{{/.}}'
        )
    });
</script>
        </div>
    </div>
</div></span>
            </div>
        </div>
        <div class="pane pane--navigation">
            <div class="pane_inner">
                <span class='NavigationPaneDiv10'><nav class="nav nav--mobile"><ul class="level1">
	<li class="has-children"><a href="https://www.barrick.com/English/about/default.aspx">About</a><ul class="level2">
		<li><a href="https://www.barrick.com/English/about/management/default.aspx">Management</a></li><li><a href="https://www.barrick.com/English/about/governance/default.aspx">Governance & Board of Directors</a></li><li><a href="https://www.barrick.com/English/contact-us/default.aspx">Contact Us</a></li>
	</ul></li><li class="has-children"><a href="https://www.barrick.com/English/operations/default.aspx">Operations</a><ul class="level2">
		<li><a href="https://www.barrick.com/English/operations/nevada-gold-mines/default.aspx">Nevada Gold Mines</a></li><li><a href="https://www.barrick.com/English/operations/Bulyanhulu/default.aspx">Bulyanhulu</a></li><li><a href="https://www.barrick.com/English/operations/Buzwagi/default.aspx">Buzwagi</a></li><li><a href="https://www.barrick.com/English/operations/hemlo/default.aspx">Hemlo</a></li><li><a href="https://www.barrick.com/English/operations/jabal-sayid/default.aspx">Jabal Sayid</a></li><li><a href="https://www.barrick.com/English/operations/kibali/default.aspx">Kibali</a></li><li><a href="https://www.barrick.com/English/operations/loulo-gounkoto/default.aspx">Loulo-Gounkoto</a></li><li><a href="https://www.barrick.com/English/operations/lumwana/default.aspx">Lumwana</a></li><li><a href="https://www.barrick.com/English/operations/North-Mara/default.aspx">North Mara</a></li><li><a href="https://www.barrick.com/English/operations/porgera/default.aspx">Porgera</a></li><li><a href="https://www.barrick.com/English/operations/pueblo-viejo/default.aspx">Pueblo Viejo</a></li><li><a href="https://www.barrick.com/English/operations/tongon/default.aspx">Tongon</a></li><li><a href="https://www.barrick.com/English/operations/veladero/default.aspx">Veladero</a></li><li><a href="https://www.barrick.com/English/operations/zaldivar/default.aspx">Zaldívar</a></li><li><a href="https://www.barrick.com/English/operations/exploration-and-projects/default.aspx">Exploration & Projects</a></li>
	</ul></li><li class="has-children"><a href="https://www.barrick.com/English/sustainability/default.aspx">Sustainability</a><ul class="level2">
		<li><a href="https://www.barrick.com/English/sustainability/our-approach/default.aspx">Our Approach</a></li><li><a href="https://www.barrick.com/English/sustainability/social-and-economic-development/default.aspx">Social & Economic Development</a></li><li><a href="https://www.barrick.com/English/sustainability/health-and-safety/default.aspx">Health & Safety</a></li><li><a href="https://www.barrick.com/English/sustainability/human-rights/default.aspx">Human Rights</a></li><li><a href="https://www.barrick.com/English/sustainability/environment/default.aspx">Environment</a></li><li><a href="https://www.barrick.com/sustainability/environment/default.aspx#tailings">Tailings Management</a></li><li><a href="https://www.barrick.com/English/sustainability/reports-policies/default.aspx">Reports & Policies</a></li>
	</ul></li><li class="has-children"><a href="https://www.barrick.com/English/investors/default.aspx">Investors</a><ul class="level2">
		<li><a href="https://www.barrick.com/English/investors/annual-report/default.aspx">Annual Report</a></li><li><a href="https://www.barrick.com/English/investors/agm/default.aspx">Annual Meeting</a></li><li><a href="https://www.barrick.com/English/investors/presentations-reports/default.aspx">Presentations & Reports</a></li><li><a href="/news/default.aspx#investors">Press Releases</a></li><li><a href="https://www.barrick.com/English/investors/shares-dividends/default.aspx">Shares & Dividends</a></li><li><a href="https://apps.indigotools.com/IR/IAC/?Ticker=GOLD&amp;Exchange=NYSE" target="_blank">Analyst Centre</a></li>
	</ul></li><li><a href="https://www.barrick.com/English/careers/default.aspx">Careers</a></li><li class="selected"><a href="https://www.barrick.com/English/news/default.aspx">News</a></li>
</ul></nav></span>
            </div>
        </div>
        <div class="pane pane--banner height--full height--ab">
            <div class="pane_inner">
                <div class="screen-wrapper">
                    <div class="screen" id="banner-tv"></div>
                </div>
                <div class="module_container--outer clearfix">
                    <div class="box box--left background--grey floating">
                        <span class='HeaderPane2Div1'><div id="_ctrl0_ctl63_divModuleContainer" class="module module-html module-page-title">
    <div class="module_container module_container--outer">
        
        <div class="module_container module_container--inner">
            <h1 class="heading--big2 no-margin" style="text-transform: none;">ANNUAL REPORT</h1>
<h2>After a year of building a strong foundation in 2019, Barrick looks to the next phase of value creation.</h2>
        </div>
    </div>
</div></span><span class='HeaderPane2Div2'><div id="_ctrl0_ctl66_divModuleContainer" class="module module-html module-intro-text">
    <div class="module_container module_container--outer">
        
        <div class="module_container module_container--inner">
            <!-- <a href="//barrick.q4cdn.com/788666289/files/doc_news/2019/08/Strong-Q2-Points-to-Annual-Production-at-Top-End-of-Guidance-Range-for-Barrick.pdf" class="button button--go color--yellow">Q3 Report</a><br> -->

<br><a href="/investors/annual-report/default.aspx" class="button button--go" color="#656565" style="line-height: 1; margin: 0;">Read the annual report</a><br>

<a href="/sustainability/default.aspx" class="button button--go" color="#656565" style="line-height: 1; margin:0;">Read the sustainability report</a><br>&nbsp;
        </div>
    </div>
</div></span>
                    </div>
                </div>
            </div>
        </div>
        <div class="layout_content" id="maincontent">
            <div class="pane pane--left">
                <div class="pane_inner">
                    <span class='LeftPaneDiv'></span>
                </div>
            </div>
            <div class="pane pane--content">
                <div class="pane_inner">
                    <span class='ContentPaneDiv'><span class='ContentPaneDiv3'><div id="_ctrl0_ctl69_divModuleContainer" class="module module-embed module-news module-news--loadmore background--grey module--no-padding-top">
    <div class="module_container module_container--outer">
        
        <div class="module_container module_container--inner">
            <div class="module_options background--grey">
    <label class="module_options-label sr-only" for="TopicSelect">Select:</label>
    <select class="module_options-select module_options-select--topic module_options-select--tag" id="TopicSelect" style="width: 200px;">
        <option value="-1">Topic</option>
        <option value="investors">Press Release</option>
        <option value="mining">Mining</option>
        <option value="innovation">Innovation</option>
        <option value="communities">Communities</option>
        <option value="education">Education</option>
        <option value="environment">Environment</option>
        <option value="partnership">Partnership</option>
<!--
        <option value="performance">Performance</option>
        <option value="perspectives">Perspectives</option>
        <option value="profile">Profile</option>
-->
    </select>
    <label class="module_options-label sr-only" for="CountrySelect">Select:</label>
    <select class="module_options-select module_options-select--country module_options-select--tag" id="CountrySelect" style="width: 240px;">
        <option value="-1">Country</option>
        <option value="argentina">Argentina</option>
<!--
        <option value="australia">Australia</option>
-->
        <option value="canada">Canada</option>
        <option value="chile">Chile</option>
       <option value="civ">Côte d'Ivoire</option>
       <option value="dominican-republic">Dominican Republic</option>
        <option value="drc">Democratic Republic of Congo</option>
        <option value="mali">Mali</option>
        <option value="papua-new-guinea">Papua New Guinea</option>
        <option value="peru">Peru</option>
        <option value="saudi-arabia">Saudi Arabia</option>
        <option value="senegal">Senegal</option>
        <option value="usa">USA</option>
        <option value="zambia">Zambia</option>
    </select>
    <label class="module_options-label sr-only" for="YearSelect">Select:</label>
    <select class="module_options-year" id="YearSelect" style="width: 160px;"></select>
</div>
<div class="module_container module_container--content grid--no-gutter grid--no-space "></div>
<div class="pager text-center"></div>

<script type="text/javascript" src="//barrick.q4cdn.com/788666289/files/js/q4.loadmore.js"></script>
<script type="text/javascript" src="//barrick.q4cdn.com/788666289/files/js/q4.scrollgrip.js"></script>
<script type="text/javascript">

var smartTags = function(options) {

    // options: {checkHash: true}

    var topicsArr = [];

    $.each(newstags.topics, function(i, item) {
        if (item.tag != '' && item.tag != undefined && item.tag != null) {
            topicsArr.push(item.tag);
        }
    });

    var hash = window.location.hash.split("#").pop();
    if( hash != '' && $.inArray(hash, topicsArr) && options.checkHash){
        if( $('.module_options-select--topic option[value*="'+hash+'"]').length ){
            $('.module_options-select--topic').val(hash).trigger('change.select2');
            return [hash];
        }
    }
    return '';
};

$('.module-news').news({
    tags: smartTags({checkHash: true}),
    titleLength: 0,
    itemContainer: '.module_container--content',
    yearSelect: '.module_options-year',
    yearContainer: '.module_options-year',
    yearTemplate: '<option value="{{value}}">{{year}}</option>',
    itemTemplate: (
        '<div class="check-viewport grid_col grid_col--3-of-12 grid_col--lg-4-of-12 grid_col--lc-6-of-12 grid_col--md-12-of-12">' +
            '<div class="check-viewport-animate-this module_item module_item--card" tabindex="0">' +
                '<div class="module_item-wrap clearfix">' +
                    '<h5 class="module-news_topics">{{#topics}}{{label}} {{/topics}} <br><span class="color--light-grey">{{date}}</span></h5>' +
                    '<a href="{{url}}" class="module-news_thumb-topic"{{#thumb}} style="background-image:url({{thumb}});background-size:cover;"{{/thumb}}></a>' +
                    '<div class="module_headline">' +
                        '<a class="module_headline-link" href="{{url}}">{{{title}}}</a>' +
                    '</div>' +
                    '<a class="module_more-link button button--go" href="{{url}}">Read more</a>' +
                '</div>' +
            '</div>' +
        '</div>'
    ),
    beforeRenderItems: function(e, data) {
        // check for specific topics
        newstags.addTopicsToItems(data.items);
    },
    itemsComplete: function(e) {
        $(e.target).loadmore({
            content: '.module_item',
            appendTo: $(e.target).find('.pager'),
            triggerClass: 'button button--loadmore',
            perPage: 16,
            afterReveal: function(){
                //force show items if in viewport
                $(window).trigger('scroll');
            }
        });

        if(!q4App.isMobile.any()) {
            //hover effect
            $(e.target).find('.module_item').append('<div class="hover-panel"></div>');
            $(e.target).find('.module_item').each( function() { $(this).hoverdir2(); } );
        }

        //force show items if in viewport
        $(window).trigger('scroll');
        if(q4App != undefined){q4App.appendAnimatedIcons([$(e.target).find('.button--go'), $(e.target).find('.button--loadmore')]);}
    },
    complete: function(e){
        $(e.target).find('.module_options').scrollGrip();
    }
});

$('.module_options').on('change.select', '.module_options-select', function(e) {
    var _ = $(this);
    //reset siblings to placeholders
    _.siblings('.module_options-select--tag').val('-1').trigger('change.select2');
    //set tag
    $('.module-news').news('setTags', _.val() == '-1' ? smartTags({checkHash: false}) : _.val());
});

</script>
        </div>
    </div>
</div></span></span>
                </div>
            </div>
            <div class="pane pane--right">
                <div class="pane_inner">
                    <span class='RightPaneDiv'></span>
                </div>
            </div>
        </div>
        <div class="layout_footer" role="contentinfo">
            <div class="pane pane--footer">
                <div class="pane_inner">
                    <span class='FooterPaneDiv'><span class='FooterPaneDiv4'><div id="_ctrl0_ctl72_divModuleContainer" class="module module-embed">
    <div class="module_container module_container--outer">
        
        <div class="module_container module_container--inner">
            <script>
    $('.PageNews .pane--banner').css('background-image','url("//barrick.q4cdn.com/788666289/files/design/banner/2020/news-032020.jpg")');
    $('.PageNews .pane--banner').css('background-position', 'initial');
  </script>
  
        </div>
    </div>
</div></span></span>
                </div>
            </div>
            <div class="pane pane--footer2">
                <div class="pane_inner background--grey clearfix">
                    <span class='FooterPane2Div14'><div id="_ctrl0_ctl39_RightBlock" class="hidden"></div>
<div id="_ctrl0_ctl39_divModuleContainer" class="module module-links list--reset module-links--social circle-icon">
    <div class="module_container module_container--outer">
        
        <div class="module_container module_container--inner">
            <ul id="_ctrl0_ctl39_qlList" class="module-links_list">
                
                        <li id="_ctrl0_ctl39_QuickLinkList_ctl00_liQuickLink" class="QuickLinkRow">
                            
                            
                            <a href="https://www.facebook.com/barrick.gold.corporation" id="_ctrl0_ctl39_QuickLinkList_ctl00_link" class="module-links_list-item-link" target="_blank"><i class="q4-icon_facebook"></i><span class="sr-only">Facebook</span></a>
                            
                        </li>
                    
                        <li id="_ctrl0_ctl39_QuickLinkList_ctl01_liQuickLink" class="QuickLinkRowAlt">
                            
                            
                            <a href="https://www.instagram.com/barrickgold/" id="_ctrl0_ctl39_QuickLinkList_ctl01_link" class="module-links_list-item-link" target="_blank"><i class="q4-icon_instagram"></i><span class="sr-only">Instagram</span></a>
                            
                        </li>
                    
                        <li id="_ctrl0_ctl39_QuickLinkList_ctl02_liQuickLink" class="QuickLinkRow">
                            
                            
                            <a href="https://www.linkedin.com/company/barrick-gold-corporation" id="_ctrl0_ctl39_QuickLinkList_ctl02_link" class="module-links_list-item-link" target="_blank"><i class="q4-icon_linkedin"></i><span class="sr-only">LinkedIn</span></a>
                            
                        </li>
                    
                        <li id="_ctrl0_ctl39_QuickLinkList_ctl03_liQuickLink" class="QuickLinkRowAlt">
                            
                            
                            <a href="https://twitter.com/BarrickGold" id="_ctrl0_ctl39_QuickLinkList_ctl03_link" class="module-links_list-item-link" target="_blank"><i class="q4-icon_twitter"></i><span class="sr-only">Twitter</span></a>
                            
                        </li>
                    
            </ul>
        </div>
    </div>
</div></span><span class='FooterPane2Div15'><div id="_ctrl0_ctl42_divModuleContainer" class="module module-subscribe module-subscribe--fancy module-subscribe--footer">
    <div class="module_container module_container--outer">
        
        <div class="module_container module_container--inner">
            <div id="_ctrl0_ctl42_validationsummary" class="module_error-container" style="display:none;">

</div>
            <div class="clearfix">
	            <h2 class="module_title"><span class="ModuleTitle">Subscribe</span></h2>
	            <table id="_ctrl0_ctl42_tableMailingLists" class="module-subscribe_table module-subscribe_mailing-list">
	<tr id="_ctrl0_ctl42_rowMailingListLabel" class="module-subscribe_table-input module-subscribe_list-header">
		<td id="_ctrl0_ctl42_ctl00">
	                        <label for="_ctrl0_ctl42_chkLists" id="_ctrl0_ctl42_lblMailingListsText">Mailing Lists</label>
	                        <span id="_ctrl0_ctl42_lblRequiredMailingLists" class="module_required">*</span>
	                    </td>
	</tr>
	<tr id="_ctrl0_ctl42_rowMailingLists" class="module-subscribe_table-input module-subscribe_list">
		<td id="_ctrl0_ctl42_ctl01">
	                        <table id="_ctrl0_ctl42_chkLists">
			<tr>
				<td><input id="_ctrl0_ctl42_chkLists_0" type="checkbox" name="_ctrl0$ctl42$chkLists$0" value="31" /><label for="_ctrl0_ctl42_chkLists_0">News Alerts</label></td>
			</tr>
		</table>
	                        
	                        <span id="_ctrl0_ctl42_cusvalMailingListsValidator" style="display:none;"></span>
	                    </td>
	</tr>
</table>

	        </div>
            <table class="module-subscribe_table module-subscribe_form">
                
                
                <tr id="_ctrl0_ctl42_rowEmailAddress" class="module-subscribe_table-input module-subscribe_email">
	<td id="_ctrl0_ctl42_ctl04">
                        <label for="_ctrl0_ctl42_txtEmail" id="_ctrl0_ctl42_lblEmailAddressText">Email Address</label>
                        <span id="_ctrl0_ctl42_lblRequiredEmailAddress" class="module_required">*</span>
                        <input name="_ctrl0$ctl42$txtEmail" type="text" maxlength="128" id="_ctrl0_ctl42_txtEmail" class="module_input" placeholder="Email Address" />
                        <span id="_ctrl0_ctl42_regexEmailValidator1" style="display:none;"></span>
                        <span id="_ctrl0_ctl42_reqvalEmailValidator1" style="display:none;"></span>
                    </td>
</tr>

                
                
                
                
                
                
                
                
                
                
                
                
                
                
            </table>
            <div class="module_actions">
                <input type="submit" name="_ctrl0$ctl42$btnSubmit" value="Submit" onclick="javascript:WebForm_DoPostBackWithOptions(new WebForm_PostBackOptions(&quot;_ctrl0$ctl42$btnSubmit&quot;, &quot;&quot;, true, &quot;d5c127be-9d5d-424e-9c12-9f9c7663fcd5&quot;, &quot;&quot;, false, false))" id="_ctrl0_ctl42_btnSubmit" class="button module-subscribe_submit-button" />
            </div>
            <div class="module_introduction"><span id="_ctrl0_ctl42_lblIntroText" class="IntroText"><p>By providing your e-mail address, you are consenting to receive press releases and other information concerning Barrick Gold Corporation and its affiliates and partners. You may withdraw your consent at any time.</p><p><small><a class="button" href="/contact-us/email-alerts/default.aspx">Unsubscribe</a></small></p></span></div>
            <div id="_ctrl0_ctl42_UCCaptcha_divModuleContainer" class="CaptchaContainer">
<table id="_ctrl0_ctl42_UCCaptcha_Table1" cellpadding="0" cellspacing="0" border="0" width="100%">
	<tr id="_ctrl0_ctl42_UCCaptcha_ctl00">
		<td id="_ctrl0_ctl42_UCCaptcha_ctl01" colspan="2">&nbsp;</td>
	</tr>
	<tr id="_ctrl0_ctl42_UCCaptcha_ctl02">
		<td id="_ctrl0_ctl42_UCCaptcha_ctl03" colspan="2"><img src="https://www.barrick.com/q4api/v4/captcha?clientId=_ctrl0_ctl42_UCCaptcha" id="_ctrl0_ctl42_UCCaptcha_Image1" /></td>
	</tr>
	<tr id="_ctrl0_ctl42_UCCaptcha_ctl04">
		<td id="_ctrl0_ctl42_UCCaptcha_ctl05" colspan="2"><b>Enter the code shown above.</b></td>
	</tr>
	<tr id="_ctrl0_ctl42_UCCaptcha_ctl06">
		<td id="_ctrl0_ctl42_UCCaptcha_ctl07" colspan="2">
			<input name="_ctrl0$ctl42$UCCaptcha$txtCode" type="text" id="_ctrl0_ctl42_UCCaptcha_txtCode" /><span id="_ctrl0_ctl42_UCCaptcha_RequiredFieldValidator1" style="display:none;">*</span>
		</td>
	</tr>
</table>

</div>
        </div>
    </div>
</div>
<div id="_ctrl0_ctl42_divEditSubscriberConfirmation" class="module module-subscribe module_confirmation-container" style="DISPLAY:none;">
    <div class="module_container module_container--outer">
        <h2 class="module_title">Email Alert Sign Up Confirmation</h2>
        <div class="module_container module_container--inner">
            
        </div>
    </div>
</div></span><span class='FooterPane2Div16'><div id="_ctrl0_ctl45_divModuleContainer" class="module module-html module-logo-footer">
    <div class="module_container module_container--outer">
        
        <div class="module_container module_container--inner">
            <a href="/home/default.aspx">
    <img src="//barrick.q4cdn.com/788666289/files/design/svg/BARRICK-GOLD-logo.svg" alt="Barrick Logo">
</a>
        </div>
    </div>
</div></span><span class='FooterPane2Div17'><div id="_ctrl0_ctl48_divModuleContainer" class="module module-html module-copyright">
    <div class="module_container module_container--outer">
        
        <div class="module_container module_container--inner">
            <span class="copyright_c">©</span> <span class="copyright_year"></span> Barrick Gold Corporation
        </div>
    </div>
</div></span><span class='FooterPane2Div18'><div id="_ctrl0_ctl51_RightBlock" class="hidden"></div>
<div id="_ctrl0_ctl51_divModuleContainer" class="module module-links list--reset module-links--footer">
    <div class="module_container module_container--outer">
        
        <div class="module_container module_container--inner">
            <ul id="_ctrl0_ctl51_qlList" class="module-links_list">
                
                        <li id="_ctrl0_ctl51_QuickLinkList_ctl00_liQuickLink" class="QuickLinkRow">
                            
                            
                            <a href="https://www.barrick.com/English/contact-us/default.aspx" id="_ctrl0_ctl51_QuickLinkList_ctl00_link" class="module-links_list-item-link" target="_self">Contact Us</a>
                            
                        </li>
                    
                        <li id="_ctrl0_ctl51_QuickLinkList_ctl01_liQuickLink" class="QuickLinkRowAlt">
                            
                            
                            <a href="https://www.barrick.com/English/legal/default.aspx" id="_ctrl0_ctl51_QuickLinkList_ctl01_link" class="module-links_list-item-link" target="_self">Legal & Privacy</a>
                            
                        </li>
                    
            </ul>
        </div>
    </div>
</div></span><span class='FooterPane2Div19'><div id="_ctrl0_ctl54_divModuleContainer" class="module module-html module-logos list--reset">
    <div class="module_container module_container--outer">
        
        <div class="module_container module_container--inner">
            <ul>
	<li><a href="https://www.icmm.com" target="_blank"><i class="q4-icon_ICMM-logo"></i><span class="sr-only">International Council on Mining &amp; Metals</span></a></li>
	<li><a href="http://www.gold.org/" target="_blank"><i class="q4-icon_WGC-logo"></i><span class="sr-only">World Gold Council</span></a></li>
</ul>
        </div>
    </div>
</div></span>
                </div>
            </div>
            <div class="pane pane--credits">
                <div class="pane_inner">
                    <span class='Q4FooterDiv20'><div id="_ctrl0_ctl57_divModuleContainer" class="module module-html module-back-to-top">
    <div class="module_container module_container--outer">
        
        <div class="module_container module_container--inner">
            <i class="q4-icon_go-top"></i>
<span class="module-back-to-top_text">Top</span>
        </div>
    </div>
</div></span><span class='Q4FooterDiv21'><div id="_ctrl0_ctl60_divModuleContainer" class="module module-embed hidden">
    <div class="module_container module_container--outer">
        
        <div class="module_container module_container--inner">
            <script type="text/javascript" src="//barrick.q4cdn.com/788666289/files/js/jquery.hoverdir2.js"></script>
<script type="text/javascript">

if( typeof newsTag === 'undefined' || !newsTag ){
    newsTagChecked = ''
} else {
    newsTagChecked = newsTag
}

if( typeof newsLimit === 'undefined' || !newsLimit ){
    newsLimitChecked = 4
} else {
    newsLimitChecked = newsLimit
}

$('.module-news-latest-topic-thumb').news({
    tags: newsTagChecked,
    limit: newsLimitChecked,
    titleLength: 0,
    showAllYears: true,
    itemContainer: '.module_items',
    itemTemplate: (
        '<div class="grid_col grid_col--3-of-12">' +
            '<div class="module_item module_item--card" tabindex="0">' +
                '<div class="module_item-wrap clearfix">' +
                    '<h5>{{#topics}}<a class="color--inherit" href="/news/default.aspx#{{tag}}">{{label}}</a> {{/topics}}</h5>' +
                    '<a href="{{url}}" class="module-news_thumb-topic"{{#thumb}} style="background-image:url({{thumb}});background-size:cover;"{{/thumb}}></a>' +
                    '<div class="module_headline">' +
                        '<a class="module_headline-link" href="{{url}}">{{title}}</a>' +
                    '</div>' +
                    '<a class="module_more-link button button--go" href="{{url}}">Read more</a>' +
                '</div>' +
            '</div>' +
        '</div>'
    ),
    beforeRenderItems: function(e, data) {
        // check for specific topics
        newstags.addTopicsToItems(data.items);
    },
    complete: function(e) {
        if(q4App != undefined){q4App.appendAnimatedIcons([$(e.target).find('.button--go')]);}

        $(e.target).find('.module_items').slick({
            slidesToShow: 4,
            slidesToScroll: 4,
            arrows: false,
            dots: true,
            appendDots: '.module-news-latest-topic-thumb .slick_dots',
            customPaging: function(slider, i) {
                return '<span class="dot"><span class="dot_symbol"></span></span>';
            },
            responsive: [{
                breakpoint: 1599,
                settings: {
                    slidesToShow: 3,
                    slidesToScroll: 3
                }
            }, {
                breakpoint: 1024,
                settings: {
                    slidesToShow: 2,
                    slidesToScroll: 2
                }
            }, {
                breakpoint: 767,
                settings: {
                    slidesToShow: 1,
                    slidesToScroll: 1
                }
            }]
        });

        /* Slick Accessibility Fix */
        $(e.target).find('.module_container--content').each(function(){
            if ( !$(this).find('.slick-dots').length ) {
                $('.slick-slide').each(function () { 
                    var $slide = $(this).parent(); 
                    if ($(this).attr('aria-describedby') != undefined) { 
                        $(this).removeAttr('aria-describedby'); 
                    }
                });
            }
        });

        if(!q4App.isMobile.any()) {
            setTimeout(function(){
                // hover effect
                $(e.target).find('.module_item').append('<div class="hover-panel"></div>');
                $(e.target).find('.module_item').each( function() { $(this).hoverdir2(); } );
            },300);
        }

        // normalize item height
        setHeight = new q4App.heightsNormalizer();
        setHeight.setHeights({
            elemSelector: $(e.target).find('.module_headline'),
            perRow: 999,
            updateOnResize: true,
            resizeDelay: 150,
            responsive: [{
                // breakpoints must be in correct reverse order to work properly (ex: 1024 > 768 > 480)
                // to not apply any style, set perRow = 1
                breakpoint:767,
                perRow: 1
            }]
        });
    }
});

</script>
        </div>
    </div>
</div></span>
                </div>
            </div>
        </div>
    </div>
</div>
                    <input type="hidden" name="__antiCSRF" id="__antiCSRF" value=""/>
                
<script type="text/javascript">
//<![CDATA[
var Page_ValidationSummaries =  new Array(document.getElementById("_ctrl0_ctl42_validationsummary"));
var Page_Validators =  new Array(document.getElementById("_ctrl0_ctl42_cusvalMailingListsValidator"), document.getElementById("_ctrl0_ctl42_regexEmailValidator1"), document.getElementById("_ctrl0_ctl42_reqvalEmailValidator1"), document.getElementById("_ctrl0_ctl42_UCCaptcha_RequiredFieldValidator1"));
//]]>
</script>

<script type="text/javascript">
//<![CDATA[
var _ctrl0_ctl42_validationsummary = document.all ? document.all["_ctrl0_ctl42_validationsummary"] : document.getElementById("_ctrl0_ctl42_validationsummary");
_ctrl0_ctl42_validationsummary.headertext = "<p class=\'module_message module_message--error\'>The following errors must be corrected:</p>";
_ctrl0_ctl42_validationsummary.displaymode = "List";
_ctrl0_ctl42_validationsummary.validationGroup = "d5c127be-9d5d-424e-9c12-9f9c7663fcd5";
var _ctrl0_ctl42_cusvalMailingListsValidator = document.all ? document.all["_ctrl0_ctl42_cusvalMailingListsValidator"] : document.getElementById("_ctrl0_ctl42_cusvalMailingListsValidator");
_ctrl0_ctl42_cusvalMailingListsValidator.errormessage = "Mailing list selection is required.";
_ctrl0_ctl42_cusvalMailingListsValidator.display = "None";
_ctrl0_ctl42_cusvalMailingListsValidator.validationGroup = "d5c127be-9d5d-424e-9c12-9f9c7663fcd5";
_ctrl0_ctl42_cusvalMailingListsValidator.evaluationfunction = "CustomValidatorEvaluateIsValid";
var _ctrl0_ctl42_regexEmailValidator1 = document.all ? document.all["_ctrl0_ctl42_regexEmailValidator1"] : document.getElementById("_ctrl0_ctl42_regexEmailValidator1");
_ctrl0_ctl42_regexEmailValidator1.controltovalidate = "_ctrl0_ctl42_txtEmail";
_ctrl0_ctl42_regexEmailValidator1.errormessage = "Email address is not valid.";
_ctrl0_ctl42_regexEmailValidator1.display = "None";
_ctrl0_ctl42_regexEmailValidator1.validationGroup = "d5c127be-9d5d-424e-9c12-9f9c7663fcd5";
_ctrl0_ctl42_regexEmailValidator1.evaluationfunction = "RegularExpressionValidatorEvaluateIsValid";
_ctrl0_ctl42_regexEmailValidator1.validationexpression = "^([a-zA-Z0-9_\\-\\.]+)@((\\[[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.)|(([a-zA-Z0-9\\-]+\\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\\]?)$";
var _ctrl0_ctl42_reqvalEmailValidator1 = document.all ? document.all["_ctrl0_ctl42_reqvalEmailValidator1"] : document.getElementById("_ctrl0_ctl42_reqvalEmailValidator1");
_ctrl0_ctl42_reqvalEmailValidator1.controltovalidate = "_ctrl0_ctl42_txtEmail";
_ctrl0_ctl42_reqvalEmailValidator1.errormessage = "Email address is required.";
_ctrl0_ctl42_reqvalEmailValidator1.display = "None";
_ctrl0_ctl42_reqvalEmailValidator1.validationGroup = "d5c127be-9d5d-424e-9c12-9f9c7663fcd5";
_ctrl0_ctl42_reqvalEmailValidator1.evaluationfunction = "RequiredFieldValidatorEvaluateIsValid";
_ctrl0_ctl42_reqvalEmailValidator1.initialvalue = "";
var _ctrl0_ctl42_UCCaptcha_RequiredFieldValidator1 = document.all ? document.all["_ctrl0_ctl42_UCCaptcha_RequiredFieldValidator1"] : document.getElementById("_ctrl0_ctl42_UCCaptcha_RequiredFieldValidator1");
_ctrl0_ctl42_UCCaptcha_RequiredFieldValidator1.controltovalidate = "_ctrl0_ctl42_UCCaptcha_txtCode";
_ctrl0_ctl42_UCCaptcha_RequiredFieldValidator1.focusOnError = "t";
_ctrl0_ctl42_UCCaptcha_RequiredFieldValidator1.errormessage = "Please provide the code.";
_ctrl0_ctl42_UCCaptcha_RequiredFieldValidator1.display = "Dynamic";
_ctrl0_ctl42_UCCaptcha_RequiredFieldValidator1.validationGroup = "d5c127be-9d5d-424e-9c12-9f9c7663fcd5";
_ctrl0_ctl42_UCCaptcha_RequiredFieldValidator1.evaluationfunction = "RequiredFieldValidatorEvaluateIsValid";
_ctrl0_ctl42_UCCaptcha_RequiredFieldValidator1.initialvalue = "";
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
