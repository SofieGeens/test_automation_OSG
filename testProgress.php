<!DOCTYPE html>
<html>
	<head>
		<title>Test progress</title>
		<style>table, th, td {border: 1px solid black; border-collapse: collapse;} td{text-align: center;}</style>
	</head>
	<body>
		<form method='post' name='progress' action='endTest.php'>
			<?php
				error_reporting(E_ERROR | E_PARSE);
				$fileName = $_POST["fileName"];
				if(!empty($fileName)){
					setcookie("fileName", $fileName, time() + (3600));
				}
				else{
					$fileName = $_COOKIE["fileName"];
				}
				$conn = mysqli_connect("127.0.0.1",getenv('MYSQLUSER_OSG'),getenv('MYSQLPASSWORD_OSG'),"masterproef");
				$query = "SELECT serialNumber FROM progress";
				$serial = mysqli_query($conn,$query);
				$serial = mysqli_fetch_array($serial,MYSQLI_ASSOC);
				$query = "SELECT oxysig FROM progress";
				$oxysig = mysqli_query($conn,$query);
				$oxysig = mysqli_fetch_array($oxysig,MYSQLI_ASSOC);
				$query = "SELECT oxy FROM progress";
				$oxy = mysqli_query($conn,$query);
				$oxy = mysqli_fetch_array($oxy,MYSQLI_ASSOC);
				$query = "SELECT bodypos FROM progress";
				$bodypos = mysqli_query($conn,$query);
				$bodypos = mysqli_fetch_array($bodypos,MYSQLI_ASSOC);
				$query = "SELECT impRef FROM progress";
				$impRef = mysqli_query($conn,$query);
				$impRef = mysqli_fetch_array($impRef,MYSQLI_ASSOC);
				$query = "SELECT impAct FROM progress";
				$impAct = mysqli_query($conn,$query);
				$impAct = mysqli_fetch_array($impAct,MYSQLI_ASSOC);
				$query = "SELECT sig FROM progress";
				$sig = mysqli_query($conn,$query);
				$sig = mysqli_fetch_array($sig,MYSQLI_ASSOC);
				$query = "SELECT sigBip FROM progress";
				$sigBip = mysqli_query($conn,$query);
				$sigBip = mysqli_fetch_array($sigBip,MYSQLI_ASSOC);
				$query = "SELECT cb FROM progress";
				$cb = mysqli_query($conn,$query);
				$cb = mysqli_fetch_array($cb,MYSQLI_ASSOC);
				$query = "SELECT press FROM progress";
				$press = mysqli_query($conn,$query);
				$press = mysqli_fetch_array($press,MYSQLI_ASSOC);
				$colors = ['white','orange','green','red'];
			?>
			<p>Test of device with serial number: <?php echo $serial["serialNumber"] ?></p>
			<table style="width:100%;">
				<tr>
					<td style="background-color:<?php echo $colors[$oxysig["oxysig"]];?>"><p>Oxymeter signal</p></td>
					<td style="background-color:<?php echo $colors[$cb["cb"]];?>"><p>Data transition</p></td>
					<td style="background-color:<?php echo $colors[$impRef["impRef"]];?>"><p>Reference impedance</p></td>
					<td style="background-color:<?php echo $colors[$impAct["impAct"]];?>"><p>Active impedance</p></td>
					<td style="background-color:<?php echo $colors[$oxy["oxy"]];?>"><p>Oxymeter values</p></td>
					<td style="background-color:<?php echo $colors[$sig["sig"]];?>"><p>Reference signals</p></td>
					<td style="background-color:<?php echo $colors[$sigBip["sigBip"]];?>"><p>Bipolar signals</p></td>
					<td style="background-color:<?php echo $colors[$press["press"]];?>"><p>Pdiff and Pgage</p></td>
					<td style="background-color:<?php echo $colors[$press["press"]];?>"><p>Bodyposition</p></td>
				</tr>
			</table>
			<input type='hidden' name='fileName' value=<?php echo $fileName?> />
			<table style="width:300px; border:None;">
				<?php
					if($press["press"]==1){
						echo "<tr style='border:None;'>
							<td style='border:None; text-align: left;'><p>Check the bodyposition</p></td>
							<td style='border:None; text-align: left;'><input type='radio' name='bodpos' value='yes'/> Yes 
							<input type='radio' name='bodpos' value='no'/> No </td>
							</tr>";
						echo "<tr style='border:None;'>
							<td style='border:None; text-align: left;'><p>Check Pdiff</p></td>
							<td style='border:None; text-align: left;'><input type='radio' name='Pdiff' value='yes'/> Yes 
							<input type='radio' name='Pdiff' value='no'/> No </td>
							</tr>";
						echo "<tr style='border:None;'>
							<td style='border:None; text-align: left;'><p>Check Pgage</p></td>
							<td style='border:None; text-align: left;'><input type='radio' name='Pgage' value='yes'/> Yes 
							<input type='radio' name='Pgage' value='no'/> No </td>
							</tr></table>";
						echo "please close the current measurement before ending the test";
						echo "<input type='submit' value='End test'/>";
					}
					else{
						header("refresh: 5;");
					}
					
				?>
		</form>
	</body>
</html>