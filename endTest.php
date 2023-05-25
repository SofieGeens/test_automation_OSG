<!DOCTYPE html>
<html>
	<head>
		<title>End test</title>
	</head>
	<body>
		<form method="post" name="endTest" action="startTest.php">
			<?php
				$conn = mysqli_connect("127.0.0.1",getenv('MYSQLUSER_OSG'),getenv('MYSQLPASSWORD_OSG'),"masterproef");
				$fileName = $_POST["fileName"];
				$bodypos = $_POST["bodpos"];
				$Pdiff = $_POST["Pdiff"];
				$Pgage = $_POST["Pgage"];
				$file = fopen($fileName,"a") or die("Unable to open file!");
				if($bodypos == "yes") {
					fwrite($file,"<p style='color: green;'>bodyposition ok</p>");
					$query = "UPDATE progress SET bodypos=2;";
					mysqli_query($conn,$query);
				}
				else{
					fwrite($file,"<p style='color: red;'>bodyposition not ok</p>");
					$query = "UPDATE progress SET bodypos=3;";
					mysqli_query($conn,$query);
				}
				if($Pdiff == "yes") {
					fwrite($file,"<p style='color: green;'>Pdiff ok</p>");
					$query = "UPDATE progress SET press=2;";
					mysqli_query($conn,$query);
				}
				else{
					fwrite($file,"<p style='color: red;'>Pdiff not ok</p>");
					$query = "UPDATE progress SET press=3;";
					mysqli_query($conn,$query);
				}
				if($Pgage == "yes") {
					fwrite($file,"<p style='color: green;'>Pgage ok</p>");
				}
				else{
					fwrite($file,"<p style='color: red;'>Pgage not ok</p>");
					$query = "UPDATE progress SET press=3;";
					mysqli_query($conn,$query);
				}
				$success = True;
				$query = "SELECT oxy,oxysig,bodypos,impRef,impAct,sig,sigBip,press,cb FROM progress";
				$values = mysqli_query($conn,$query);
				$values = mysqli_fetch_array($values,MYSQLI_ASSOC);
				foreach($values as $value){
					echo($value);
					if($value==3){
						$success = False;
						break;
					}
				}
				echo($success);
				if($success){
					fwrite($file,"<p style='color: green;'>All tests succeeded</p>");
				}
				else{
					fwrite($file,"<p style='color: red;'>Some fault was detected, see information above</p>");
				}
				fwrite($file,"</body></html>");
				fclose($file);
				$resultFile = substr($fileName, 0, -4);
				$resultFile = $resultFile."pdf";
				$command = 'start /B cmd /C "python C:/Users/sofie/OneDrive/Documenten/unif/2022-2023/masterproef/morpheus/makePdf.py ' . escapeshellarg($fileName) . ' ' . escapeshellarg($resultFile) . '"';
				exec($command);
			?>
			<p>The report was made succesfully"</p>
			<input type="submit" value="Start new test"/>
		</form>
	</body>
</html>
		