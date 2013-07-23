#!/usr/bin/perl
# è praticamente formmail.cgi al 100%
&form_parse;

##############################################################################
# CONFIGURATION
##############################################################################

# e-mail address to send the results to
$tomail = 'certificatori@lists.partito-pirata.it';

#path to sendmail
$mailprog ='/usr/bin/sendmail';

# page to send user to after submitting form
$sendtopage = "http://old-static.partito-pirata.it/contatto/grazie.html";

# path to temporary directory must be chmod 0777
$tempdir = "./captcha/temp";

# Define fields to exclude
# prevent captcha and submit fields from being included in the form mail results
$form{'submit'} = "exclude";

# number of seconds to block from using forms after max tries
$timetoblock = 86400; # 86400 seconds is 24 hours

# maximum number of posts allowed in the time above
$maxtries = 10;

##############################################################################
# MAIN PROGRAM
##############################################################################

# CAPTCHA verify if the image matched the form input
&checkcaptcha;

# check number of times accessed this program
&check_posts;

# only allow posts to this script
if($ENV{"REQUEST_METHOD"} ne "POST") {
	print "Content-Type: text/html\n\n";
	print "invalid access method";
	exit;
	}



&mail_results;


# send user to location or page
print "Location: $sendtopage\n\n";

exit;


# e-mail subs

sub mail_results {

$fromail = "contatto\@partito-pirata.it";
	
      open( MAIL, "|$mailprog -t" );
      print MAIL "Subject: CONTATTO\n";
      print MAIL "From: $fromail\n";
      print MAIL "To: $tomail\n";
      print MAIL "Reply-to: $tomail\n\n";

      #print MAIL "----------------------------\n\n";
      &all_fields;
      #print MAIL "\n\n----------------------------\n\n";
      close MAIL;


}


# Print all the variables on the form
sub all_fields {

# exclude the captcha image text
$form{'verifytext'} = "exclude";	

## Print all the variables in the mail
undef %is_exclude;
for (@exclude) { $is_exclude{$_} = 1 }

      foreach $key (keys %form) {
         # Print the name and value pairs in FORM array to MAIL.
         print MAIL "$key: $form{$key}\n\n" unless ($form{$key} eq "exclude");
         
      }
      
      foreach $key (keys %form) {
         # Print the name and value pairs in FORM array to MAIL.
         #XML
         print MAIL "<$key>$form{$key}<\/$key>\n" unless ($form{$key} eq "exclude");
      }      
      
}




# captcha uses everything below this line

sub checkcaptcha {
	
# use this program to remove all old temp files
# this keeps the director clean without setting up a cron job
opendir TMPDIR, "$tempdir"; 
@alltmpfiles = readdir TMPDIR;

foreach $oldtemp (@alltmpfiles) {

        $age = 0;
        $age = (stat("$tempdir/$oldtemp"))[9];
        # if age is more than 18000 seconds or 5 hours  
        if ((time - $age) > 18000){unlink "$tempdir/$oldtemp";}
        
        }
	
# lets block direct access that is not via the form post
if ($ENV{"REQUEST_METHOD"} ne "POST"){&captchanopost;}	


# open the temp datafile for current user based on ip
$tempfile = "$tempdir/$ENV{'REMOTE_ADDR'}";
open (TMPFILE, "<$tempfile")|| ($nofile = 1);
(@tmpfile) = <TMPFILE>;
close TMPFILE;

# if no matching ip file check for a cookie match
# this will compensate for AOL proxy servers accessing images
if ($nofile == 1){
        
$cookieip = $ENV{HTTP_COOKIE};
$cookieip =~ /checkme=([^;]*)/;
$cookieip = $1;

if ($cookieip ne ""){
        
        $tempfile = "$tempdir/$cookieip";
        open (TMPFILE, "<$tempdir/$cookieip")|| &captchanofile;
        (@tmpfile) = <TMPFILE>;
        close TMPFILE;
}

}

$imagetext = $tmpfile[0];
chomp $imagetext;

$verifytext = $form{'verifytext'};

# set the form input to lower case
$verifytext = lc($verifytext);

# compare the form input with the file text
if ($verifytext ne "$imagetext"){&captchaerror;}

# now delete the temp file so it cannot be used again by the same user
unlink "$tempdir/$ENV{'REMOTE_ADDR'}";
unlink "$tempdir/$cookieip";

# if no error continue with the program

# log sucessful posts to limit how many can be sent
$thetime = time;
open (ATTEMPTS, ">>$tempdir/accesslog.txt");
flock(ATTEMPTS, 2);
print ATTEMPTS "$ENV{'REMOTE_ADDR'}|$thetime|\n";
flock(ATTEMPTS, 8);
close (ATTEMPTS);
	
}

sub captchaerror {
       
print "Content-type: text/html\n\n";
print "Il testo non corrisponde, ritenta....";
# now delete the temp file so it cannot be used again by the same user
unlink "$tempdir/$ENV{'REMOTE_ADDR'}";
exit;   
}

sub captchanofile {
        
print "Content-type: text/html\n\n";
print "No file found for verification.";        
exit;   
}


sub captchanopost {
        
print "Content-type: text/html\n\n";
print "Non possibile, ricarica la pagina contatto";     
exit;   
}


#################################################
# sub to prevet multiple uses of sendmail form
#################################################

sub check_posts {

# remove old data from access log
open (ATTEMPTS, "<$tempdir/accesslog.txt");
@attempts=<ATTEMPTS>;
close ATTEMPTS;

foreach $attempt (@attempts) {
	($attempt_ip,$attempt_time,$extra)=split(/\|/,$attempt);
	chomp $attempt;
	if (($attempt_time + $timetoblock) > time){push (@newattempts,$attempt);}
                        
                 }

# write current data back to access log
open (ATTEMPTS, ">$tempdir/accesslog.txt");
flock ATTEMPTS, 2;
foreach $attempt (@newattempts){
	print ATTEMPTS "$attempt\n";}
flock ATTEMPTS, 8;
close ATTEMPTS;	
		
$countposts = 0;

# compare data against all current attempts
foreach $attempt (@newattempts)	{
$attempt_ip = "";
$attempt_time = "";

($attempt_ip,$attempt_time,$extra)=split(/\|/,$attempt);

if ($ENV{'REMOTE_ADDR'} eq "$attempt_ip"){$countposts++;}

}

# if too many attempts block access to program
if ($countposts > $maxtries){
	print "Content-Type: text/html\n\n";
	print "WARNING: Hai consumato tutte le possibilita, devi attendere 24 ore per riprovare.";
	exit;}

}


sub form_parse  {
	read (STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
	@pairs = split(/&/, $buffer);

	foreach $pair (@pairs)
	{
    	($name, $value) = split(/=/, $pair);
    	$value =~ tr/+/ /;
    	$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
    	$form{$name} = $value;
	}}
