<!DOCTYPE html>
<html>
	<head>
		<title>Start test</title>
	</head>
	<body>
		<?php
			// Connect to database
			 $conn = mysqli_connect("127.0.0.1",getenv('MYSQLUSER_OSG'),getenv('MYSQLPASSWORD_OSG'),"masterproef");
			 $query = "SELECT testName FROM test";
			 $devices = mysqli_query($conn,$query);
			 $query = "SELECT name from person";
			 $people = mysqli_query($conn,$query);
		?>
		<form method="post" name="startTest" action="startTestFunctions.php">
			<table>
				<tr>
					<td><p>Device:</p></td>
					<td><select name="device">
						<?php while ($device = mysqli_fetch_array($devices,MYSQLI_ASSOC)):; ?>
						<option value="<?php echo $device["testName"];?>">
							<?php echo $device["testName"];?>
						</option>
						<?php endwhile; ?>
					</select></td>
				</tr>
				<tr><td><p>Serial number:</p></td><td><input type="text" name="serNum" size="20" maxlength="30"/></td></tr>
				<tr><td><p>Hardware version:</p></td><td><input type="text" name="HWVers" size="20" maxlength="30"/></td></tr>
				<tr><td><p>Firmware version:</p></td><td><input type="text" name="FWVers" size="20" maxlength="30"/></td></tr>
				<tr>
					<td><p>Does the serial number match the label?</p></td>
					<td><input type="radio" name="label" value="yes"/> Yes 
					<input type="radio" name="label" value="no" checked="checked"/> No </td>
				</tr>
				<tr>
					<td><p>Person taking the test:</p></td>
					<td><select name="person">
						<?php while ($names = mysqli_fetch_array($people,MYSQLI_ASSOC)):; ?>
						<option value="<?php echo $names["name"];?>">
							<?php echo $names["name"];?>
						</option>
						<?php endwhile; ?>
					</select></td>
				</tr>
			</table>
			<input type="submit" value="Start the test"/>
		</form>
	</body>
</html>