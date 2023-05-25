<?php
	$dev = $_POST["device"];
	$serial = $_POST["serNum"];
	$HW = $_POST["HWVers"];
	$FW = $_POST["FWVers"];
	$label = $_POST["label"];
	$pers = $_POST["person"];
	$fileName = "C:\Users\sofie\OneDrive\Documenten\unif\\2022-2023\masterproef\morpheus\\reports\\".$serial.".html";
	$file = fopen($fileName,"w") or die("Unable to open file!");
	fwrite($file,"<!DOCTYPE html>\n<html>\n<head>\n");
	fwrite($file,"<title>Test progress</title>\n");
	fwrite($file,"<style>table, th, td {border: 1px solid black; border-collapse: collapse;}td {width:25%;}</style>");
	fwrite($file,"</head>\n<body>\n");
	fwrite($file,"<table><tr><td>Device: ".$dev."</td><td>Serial number: ".$serial."</td></tr>");
	fwrite($file,"<tr><td>Hardware version: ".$HW."</td><td>Firmware version: ".$FW."</td></tr>");
	fwrite($file,"<tr><td>Name: ".$pers."</td><td>Date: ".date("d/m/Y")."</td></tr></table>");
	if($label == "yes") {
		fwrite($file,"<p style='color: green;'>Serial number matches label.</p>");
	}
	else{
		fwrite($file,"<p style='color: red;'>Serial number doesn't match label.</p>");
	}
	fclose($file);
	startTest($dev,$fileName,$serial);
	function startTest($device,$resultFile,$serial){
		// Connect to database
		$conn = mysqli_connect("127.0.0.1",getenv('MYSQLUSER_OSG'),getenv('MYSQLPASSWORD_OSG'),"masterproef");
		$query = "DELETE FROM progress";
		mysqli_query($conn,$query);
		$query = "INSERT INTO progress (serialNumber,oxy,oxysig,bodypos,impRef,impAct,sig,sigBip,press,cb) VALUES ('".$serial."',0,0,0,0,0,0,0,0,0);";
		mysqli_query($conn,$query);
		echo "<form method='post' name='testStarted' action='testProgress.php'>";
		echo "<p>The test was started succesfully</p>";
		echo "<input type='hidden' name='fileName' value='".$resultFile."'/>";
		echo "<input type='submit' value='View progress'/>";
		echo "</form>";
		echo "</body></html>";
		$command = 'start /B cmd /C "python C:/Users/sofie/OneDrive/Documenten/unif/2022-2023/masterproef/morpheus/startTest.py ' . escapeshellarg($device) . ' ' . escapeshellarg($resultFile) . '"';
		exec($command." > output.txt 2>error.txt");
	}
?>

