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

		<tr>
			<p>Toestel:</p>
			<select name="device">
				<?php while ($device = mysqli_fetch_array($devices,MYSQLI_ASSOC)):; ?>
				<option value="<?php echo $device["testName"];?>">
					<?php echo $device["testName"];?>
				</option>
				<?php endwhile; ?>
			</select>
		</tr>
		<tr><p>Serienummer:</p><input type="text" name="winmsg3" size="30" maxlength="80"/></tr>
		<tr><p>Hardware versie:</p><input type="text" name="winmsg2" size="30" maxlength="80"/></tr>
		<tr><p>Firmware versie:</p><input type="text" name="winmsg1" size="30" maxlength="80"/></tr>
		<tr><p>Is de serienummer hetzelfde als op het label:</p><input type="text" name="winmsg0" size="30" maxlength="80"/></tr>
		<tr>
			<p>Persoon die de test afneemt:</p>
			<select name="person">
				<?php while ($names = mysqli_fetch_array($people,MYSQLI_ASSOC)):; ?>
				<option value="<?php echo $names["name"];?>">
					<?php echo $names["name"];?>
				</option>
				<?php endwhile; ?>
			</select>
		</tr>

	</body>
</html>