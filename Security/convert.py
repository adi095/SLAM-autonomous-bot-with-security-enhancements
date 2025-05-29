import csv
import re  # For parsing text file content

def parse_cmd_vel(file_path, output_csv):
    """Convert /cmd_vel topic text file to CSV."""
    with open(file_path, 'r') as txt, open(output_csv, 'w', newline='') as csvf:
        writer = csv.writer(csvf)
        writer.writerow(['timestamp', 'linear_x', 'angular_z'])  # CSV headers

        for line in txt:
            # Extract timestamp and Twist values
            match = re.search(r"stamp:\s+sec:\s+(\d+).*nanosec:\s+(\d+).*linear:\s+x:\s+([-.\d]+).*angular:\s+z:\s+([-.\d]+)", line, re.DOTALL)
            if match:
                timestamp = int(match.group(1)) + int(match.group(2)) / 1e9
                linear_x = float(match.group(3))
                angular_z = float(match.group(4))
                writer.writerow([timestamp, linear_x, angular_z])

def parse_imu(file_path, output_csv):
    """Convert /imu topic text file to CSV."""
    with open(file_path, 'r') as txt, open(output_csv, 'w', newline='') as csvf:
        writer = csv.writer(csvf)
        writer.writerow(['timestamp', 'orientation_x', 'orientation_y', 'orientation_z', 'orientation_w',
                         'angular_velocity_x', 'angular_velocity_y', 'angular_velocity_z',
                         'linear_acceleration_x', 'linear_acceleration_y', 'linear_acceleration_z'])

        for line in txt:
            # Extract timestamp and IMU values
            match = re.search(
                r"stamp:\s+sec:\s+(\d+).*nanosec:\s+(\d+).*orientation:\s+x:\s+([-.\d]+).*y:\s+([-.\d]+).*z:\s+([-.\d]+).*w:\s+([-.\d]+).*angular_velocity:\s+x:\s+([-.\d]+).*y:\s+([-.\d]+).*z:\s+([-.\d]+).*linear_acceleration:\s+x:\s+([-.\d]+).*y:\s+([-.\d]+).*z:\s+([-.\d]+)",
                line, re.DOTALL)
            if match:
                timestamp = int(match.group(1)) + int(match.group(2)) / 1e9
                orientation = [float(match.group(i)) for i in range(3, 7)]
                angular_velocity = [float(match.group(i)) for i in range(7, 10)]
                linear_acceleration = [float(match.group(i)) for i in range(10, 13)]
                writer.writerow([timestamp] + orientation + angular_velocity + linear_acceleration)

def parse_scan(file_path, output_csv):
    """Convert /scan topic text file to CSV."""
    with open(file_path, 'r') as txt, open(output_csv, 'w', newline='') as csvf:
        writer = csv.writer(csvf)
        writer.writerow(['timestamp', 'angle_min', 'angle_max', 'range_min', 'range_max', 'ranges'])

        buffer = ""
        for line in txt:
            # Accumulate lines until full message is captured (to handle multi-line entries)
            buffer += line.strip() + " "
            if "---" in line:  # End of message delimiter
                # Extract timestamp and LaserScan values
                match = re.search(
                    r"stamp:\s+sec:\s+(\d+).*nanosec:\s+(\d+).*angle_min:\s+([-.\d]+).*angle_max:\s+([-.\d]+).*range_min:\s+([-.\d]+).*range_max:\s+([-.\d]+).*ranges:\s+\[(.*?)\]",
                    buffer, re.DOTALL)
                if match:
                    timestamp = int(match.group(1)) + int(match.group(2)) / 1e9
                    angle_min = float(match.group(3))
                    angle_max = float(match.group(4))
                    range_min = float(match.group(5))
                    range_max = float(match.group(6))
                    ranges = match.group(7).split(',')  # Convert ranges to list
                    ranges = [float(r) for r in ranges if r.strip()]  # Filter and convert to float
                    writer.writerow([timestamp, angle_min, angle_max, range_min, range_max, ranges])
                buffer = ""  # Reset buffer for the next message

# Example usage
if __name__ == "__main__":
    # Update the paths below to the correct locations of your text files
    parse_cmd_vel('/home/adishree/turtlebot3_ws/src/topic_output.txt', 'cmd_vel_output.csv')
    parse_imu('/home/adishree/turtlebot3_ws/src/topic_output1.txt', 'imu_output.csv')
    parse_scan('/home/adishree/turtlebot3_ws/src/topic_output2.txt', 'scan_output.csv')
