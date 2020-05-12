
<!DOCTYPE html>
<html lang="en">
<head><meta name="viewport" content="initial-scale=1, maximum-scale=1, minimum-scale=1, width=device-width" />
<meta http-equiv="cleartype" content="on" />
<!--[if gte IE 8]><!-->
<link rel="stylesheet" href="/assets/css/styles_ie9_other.css?x=45" />
<!--<![endif]-->
<!--[if lt IE 9 ]>
<link rel="stylesheet" href="/assets/css/styles_ie8.css?x=45" />
<!--<![endif]-->
<link rel="stylesheet" href="/assets/css/contentstyles.css?x=mb" />
<link rel="stylesheet" href="/assets/css/print.css" media="print" />
<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false&key=AIzaSyAXfHC7jpIlUH2O_P78sRrr__ElN4EtyGo"></script>
<script type="text/javascript" src="/assets/js/jsfuncs.js"></script>
<script type="text/javascript">

function ToggleMenu(){
	var el = document.getElementById("mobilenav");
	if(el.style.display == "block"){
		el.style.display = "none";
	}else{
		el.style.display = "block";
	}
}

function TogIt(ref){
	var uls = document.getElementsByTagName("LI");
	for(i=0;i<uls.length;i++){
		if(uls[i].className == "lev0li"){
			if(uls[i].childNodes[2]){uls[i].childNodes[2].style.display = "none";}

		}
	}
	if(ref.childNodes[2] != null && ref.childNodes[2].nodeName == "UL"){
		if(ref.childNodes[2].style.display == "block"){
			ref.childNodes[2].style.display = "none";
		}else{
			ref.childNodes[2].style.display = "block";
		}
	}
}

function TogIt2(ref){
	var list = document.getElementsByTagName("UL");
	for(i=0;i<list.length;i++){
		if(list[i].className == "level2"){
			list[i].style.display = "none";
		}
	}
	
	if(ref.childNodes[2] != null && ref.childNodes[2].nodeName == "UL"){
		if(ref.childNodes[2].style.display == "block"){
			ref.childNodes[2].style.display = "none";
		}else{
			ref.childNodes[2].style.display = "block";
		}
	}
}

</script>
<script src="/assets/js/jquery-1.9.1.min.js"></script>
<script src="/assets/js/frame-manager.js"></script>
<title> Regulatory news </title>
<meta name="author" content="Adam Minster" />
<meta name="revised" content=",Tuesday, January 22, 2013" />
<meta name="generator" content="CMS4" />
<meta name="description" content="Regulatory news" />
<meta name="keywords" content="Construction, Ashtead, equipment, rental, United States, United Kingdon" />
</head>
<body onload="DoCookie();">

<div class="wrapper">
	<div class="topall" id="topall">
		<form class="topform" action="/search/default.aspx" method="post">
		<div class="topper1"><img src="/assets/images/top-logo.gif" alt="Ashtead" /></div>
<div class="toppersright"><div class="topper2"><a href="/contactus/default.aspx">Contact us</a></div>
		<div class="topper3"><a href="/search/sitemap.aspx">Site map</a></div>
		<div class="topper4"><a href="javascript:window.print();">Print page</a></div>
		<div class="topper5"><a id="Topper5" href="/search/cookiepolicy.aspx">Cookie policy</a><img onclick="ToggleMenu();" id="MobMnBtn" src="/assets/images/mobilemenubtn.jpg" /></a></div>
		<div class="topper6"><input type="text" class="searchtext" name="searchtext" /></div>
		<div class="topper7"><input type="submit" name="searchbtn" class="searchbtn" value="Search" /></div></div>
		</form>
		
		<div class="mobilenav" id="mobilenav"><ul class="level0">
     <li><a href="/">Home</a></li>
     <li class="lev0li" ontouch="TogIt(this);" onclick="TogIt(this);"><a href="javascript:void(0);">About us</a>
     <ul class="level1">
         <li class="subtop"><a href="/aboutus/default.aspx">About us</a></li>
         <li><a href="/aboutus/ataglance.aspx">At a glance</a></li>
         <li><a href="/aboutus/whatwedo.aspx">What we do</a></li>
         <li class="pparent" ontouch="TogIt2(this);" onclick="TogIt2(this);"><a href="javascript:void(0);">Group structure</a>
         <ul class="level2">
             <li><a href="/aboutus/groupstructure.aspx">Group structure</a></li>
             <li><a href="/aboutus/sunbelt.aspx">Sunbelt</a></li>
             <li><a href="/aboutus/aplant.aspx">A-Plant</a></li>
         </ul>
         </li>
         <li class="pparent" ontouch="TogIt2(this);" onclick="TogIt2(this);"><a href="javascript:void(0);">Our strategy</a>
         <ul class="level2">
             <li><a href="/aboutus/ourbusiness.aspx">Our strategy</a></li>
             <li><a href="/aboutus/cementingthebenefitsofstructuralchange.aspx">Cementing the benefits of structural change</a></li>
             <li><a href="/aboutus/capitalisingontheopportunity.aspx">Capitalising on the opportunity</a></li>
             <li><a href="/aboutus/maximisingperformance.aspx">Maximising performance</a></li>
             <li><a href="/aboutus/businessmodel.aspx">Business model</a></li>
             <li><a href="/aboutus/visionandvalues.aspx">Vision and values</a></li>
         </ul>
         </li>
         <li class="pparent" ontouch="TogIt2(this);" onclick="TogIt2(this);"><a href="javascript:void(0);">Corporate governance</a>
         <ul class="level2">
             <li><a href="/aboutus/corporategovernance.aspx">Corporate governance</a></li>
             <li><a href="/aboutus/theboard.aspx">The Board</a></li>
             <li><a href="/aboutus/roleoftheboard.aspx">Role of the Board</a></li>
             <li><a href="/aboutus/boardcommittees.aspx">Board committees</a></li>
             <li><a href="/aboutus/termsofreference.aspx">Terms of reference</a></li>
         </ul>
         </li>
     </ul>
     </li>
     <li class="lev0li" ontouch="TogIt(this);" onclick="TogIt(this);"><a href="javascript:void(0);">Corporate responsibility</a>
     <ul class="level1">
         <li class="subtop"><a href="/corporateresponsibility/default.aspx">Corporate responsibility</a></li>
         <li><a href="/corporateresponsibility/healthandsafety.aspx">Health and safety</a></li>
         <li><a href="/corporateresponsibility/ouremployees.aspx">Our people</a></li>
         <li><a href="/corporateresponsibility/ourcustomers.aspx">Our customers</a></li>
         <li><a href="/corporateresponsibility/ashteadinthecommunity.aspx">Communities</a></li>
         <li><a href="/corporateresponsibility/ashteadandtheenvironment.aspx">Environment</a></li>
     </ul>
     </li>
     <li class="lev0li" ontouch="TogIt(this);" onclick="TogIt(this);"><a href="javascript:void(0);">Investor centre</a>
     <ul class="level1">
         <li class="subtop"><a href="/investorcentre/default.aspx">Investor centre</a></li>
         <li><a href="/investorcentre/strategy.aspx">Strategy</a></li>
         <li><a href="/investorcentre/financialhighlights.aspx">Financial highlights</a></li>
         <li><a href="/investorcentre/kpis.aspx">KPIs</a></li>
         <li><a href="/investorcentre/principalrisksanduncertainties.aspx">Principal risks and uncertainties</a></li>
         <li><a href="/investorcentre/resultsandpresentations.aspx">Results and presentations</a></li>
         <li><a href="/investorcentre/annualreports.aspx">Annual Reports</a></li>
         <li><a href="/investorcentre/detailedshareprice.aspx">Detailed share price</a></li>
         <li><a href="/investorcentre/sharepricechart.aspx">Share price chart</a></li>
         <li><a href="/investorcentre/sharepricecalculator.aspx">Share price calculator</a></li>
         <li><a href="/investorcentre/regulatorynews.aspx">Regulatory news</a></li>
         <li><a href="/investorcentre/registerforemailalerts.aspx">Register for e-mail alerts</a></li>
         <li><a href="/investorcentre/majorshareholders.aspx">Major shareholders</a></li>
         <li><a href="/investorcentre/shareholderinformation.aspx">Shareholder information</a></li>
         <li><a href="/investorcentre/noticeofmeeting.aspx">Notice of meeting</a></li>
         <li><a href="/investorcentre/dividendhistoryandcalculator.aspx">Dividend history and calculator</a></li>
         <li><a href="/investorcentre/brokerspage.aspx">Analysts</a></li>
         <li><a href="/investorcentre/investornews.aspx">Investor news</a></li>
         <li><a href="/investorcentre/webcasts.aspx">Webcasts</a></li>
         <li><a href="/investorcentre/financialcalendar.aspx">Financial calendar</a></li>
         <li><a href="/investorcentre/investorfaqs.aspx">Investor FAQs</a></li>
         <li><a href="/investorcentre/advisers.aspx">Advisers</a></li>
     </ul>
     </li>
     <li class="lev0li" ontouch="TogIt(this);" onclick="TogIt(this);"><a href="javascript:void(0);">Media centre</a>
     <ul class="level1">
         <li class="subtop"><a href="/mediacentre/default.aspx">Media centre</a></li>
         <li><a href="/mediacentre/regulatorynews.aspx">Regulatory news</a></li>
         <li><a href="/mediacentre/subscribetonewsalerts.aspx">Register for e-mail alerts</a></li>
         <li><a href="/mediacentre/ashteadgroupfactsheet.aspx">Ashtead Group fact sheet</a></li>
         <li><a href="/mediacentre/pressprcontacts.aspx">Press / PR contacts</a></li>
     </ul>
     </li>
     <li class="lev0li"><a href="/careers/default.aspx">Careers</a></li>
     <li class="lev0li"><a href="/contactus/default.aspx">Contact us</a></li>
     <li class="lev0li" ontouch="TogIt(this);" onclick="TogIt(this);"><a href="javascript:void(0);">Search</a>
     <ul class="level1">
         <li class="subtop"><a href="/search/default.aspx">Search</a></li>
         <li><a href="/search/sitemap.aspx">Sitemap</a></li>
         <li><a href="/search/cookiepolicy.aspx">Cookie policy</a></li>
         <li><a href="/search/privacy.aspx">Privacy</a></li>
         <li><a href="/search/disclaimer.aspx">Disclaimer</a></li>
         <li><a href="/search/feedback.aspx">Feedback</a></li>
         <li><a href="/search/requestinformation.aspx">Request information</a></li>
     </ul>
     </li>
</ul>
</div>

		<div class="topnav"><ul><li id="tnitm0"><a accesskey="H" href="/default.aspx">Home</a></li>
<li id="tnitm1"><a accesskey="2" href="/aboutus/default.aspx">About us</a></li>
<li id="tnitm2"><a accesskey="3" href="/corporateresponsibility/default.aspx">Corporate responsibility</a></li>
<li id="tnitm3" class="active"><a accesskey="4" href="/investorcentre/default.aspx" class="active">Investor centre</a></li>
<li id="tnitm4"><a accesskey="5" href="/mediacentre/default.aspx">Media centre</a></li>
<li id="tnitm5"><a accesskey="6" href="/careers/default.aspx">Careers</a></li>
<li id="tnitm6" class="last"><a accesskey="7" href="/contactus/default.aspx">Contact us</a></li>
</ul></div>
		
		<div class="crumbs"><ul><li class="bcli1"><a class="bcl1" href="/default.aspx">Home:</a> </li>
<li class="bcli2"><a class="bcl2" href="/investorcentre/default.aspx">Investor centre</a> </li>
<li class="bclilast"><a class="bcllast" href="/investorcentre/regulatorynews.aspx">Regulatory news</a></li>
</ul></div><div class='bigpic' style='background:transparent url(/lib/images/072557-lorryrental.png) no-repeat top left;'></div></div>
	
	<div class="main">
		<div class="mainleft"><ul class="leftnav"><li class="lnNL1"><a href="/investorcentre/default.aspx"  class="NL1" >Investor centre</a></li>
<li class="lnNL2"><a href="/investorcentre/ourbusinessmodel.aspx"  class="NL2" >Our business model</a></li>
<li class="lnNL2"><a href="/investorcentre/strategicreview.aspx"  class="NL2" >Strategic review</a></li>
<li class="lnNL2"><a href="/investorcentre/financialhighlights.aspx"  class="NL2" >Financial highlights</a></li>
<li class="lnNL2"><a href="/investorcentre/kpis.aspx"  class="NL2" >KPIs</a></li>
<li class="lnNL2"><a href="/investorcentre/principalrisksanduncertainties.aspx"  class="NL2" >Principal risks and uncertainties</a></li>
<li class="lnNL2"><a href="/investorcentre/resultsandpresentations.aspx"  class="NL2" >Results and presentations</a></li>
<li class="lnNL2"><a href="/investorcentre/annualreports.aspx"  class="NL2" >Annual Reports</a></li>
<li class="lnNL2"><a href="/investorcentre/detailedshareprice.aspx"  class="NL2" >Detailed share price</a></li>
<li class="lnNL2"><a href="/investorcentre/sharepricechart.aspx"  class="NL2" >Share price chart</a></li>
<li class="lnNL2"><a href="/investorcentre/sharepricecalculator.aspx"  class="NL2" >Share price calculator</a></li>
<li class="lnNL2"><a href="/investorcentre/sharepricehistoricdownload.aspx"  class="NL2" >Share price historic download</a></li>
<li class="active lnNL2"><a href="/investorcentre/regulatorynews.aspx"  class="active NL2" >Regulatory news</a></li>
<li class="lnNL2"><a href="/investorcentre/registerforemailalerts.aspx"  class="NL2" >Register for e-mail alerts</a></li>
<li class="lnNL2"><a href="/investorcentre/majorshareholders.aspx"  class="NL2" >Major shareholders</a></li>
<li class="lnNL2"><a href="/investorcentre/shareholderinformation.aspx"  class="NL2" >Shareholder information</a></li>
<li class="lnNL2"><a href="/investorcentre/noticeofmeeting.aspx"  class="NL2" >Notice of meeting</a></li>
<li class="lnNL2"><a href="/investorcentre/dividendhistoryandcalculator.aspx"  class="NL2" >Dividend history and calculator</a></li>
<li class="lnNL2"><a href="/investorcentre/analysts.aspx"  class="NL2" >Analysts</a></li>
<li class="lnNL2"><a href="/investorcentre/creditratingsanddebtinformation.aspx"  class="NL2" >Credit ratings and debt information</a></li>
<li class="lnNL2"><a href="/investorcentre/investornews.aspx"  class="NL2" >Investor news</a></li>
<li class="lnNL2"><a href="/investorcentre/webcasts.aspx"  class="NL2" >Webcasts</a></li>
<li class="lnNL2"><a href="/investorcentre/financialcalendar.aspx"  class="NL2" >Financial calendar</a></li>
<li class="lnNL2"><a href="/investorcentre/investorfaqs.aspx"  class="NL2" >Investor FAQs</a></li>
<li class="lnNL2"><a href="/investorcentre/advisers.aspx"  class="NL2" >Advisers</a></li>
</ul></div>
		<div class="mainfull"><h1>Regulatory news</h1>

<div class="framewrapper">
<iframe  frameborder="0" style="width:100%;height:840px;overflow:auto;" src="http://otp.investis.com/clients/uk/ashtead-group/rns/regulatory-news.aspx?culture=en-GB"></iframe>
<p>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;  &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;  &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;</p>
</div></div>
	</div>
</div>

<div class="footerouter">
	<div class="footerinner">
		<div class="footertop">
			<img class="ftlogo" src="/assets/images/bottom-logo.gif" alt="Ashtead" />
		</div>	
		<ul class="footbott">
		<li>
		<a href="/search/disclaimer.aspx" class="fnfirst">Disclaimer</a>
			<a href="/search/privacy.aspx">Privacy</a>
			<a href="/contactus/default.aspx">Contact us</a>
			<a href="/search/feedback.aspx">Feedback</a>
			<a href="/search/cookiepolicy.aspx">Cookie policy</a>
			<a href="/search/requestinformation.aspx">Request information</a>
		</li>
		<li class="dateref">2019 Ashtead Group plc. All rights reserved</li>
		<li><a class="fnfirst" href="/aboutus/modernslavery.aspx">Modern Slavery and Human Trafficking Statement</a></li>
		<li class="builderref">Designed and built by <a href="http://comprend.com" target="_blank">Comprend</a></li>
		</ul>
	</div>
</div></div>
</div>
<div id="cookiepop"><h3>Cookie Control <a href="javascript:AcceptCookie();">Accept</a></h3><p>This site uses unobtrusive cookies to store information on your computer. By using our site you accept the terms of our <a title="Privacy" href="../../search/privacy.aspx">Privacy Policy</a>.
</p> <div class="cookiemore"><a href="/search/cookiepolicy.aspx">Read more</a></div></div><script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-9404478-1', 'auto');
  ga('send', 'pageview');

</script>
</body>
</html>