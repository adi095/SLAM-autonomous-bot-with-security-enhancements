import os
import csv
from rclpy.serialization import deserialize_message
from rosidl_runtime_py.utilities import get_message
from rosbag2_py import SequentialReader, StorageOptions, ConverterOptions

def extract_rosbag2_to_single_csv(bag_path, output_csv):
    # Set up the ROS 2 bag reader
    reader = SequentialReader()
    storage_options = StorageOptions(uri=bag_path, storage_id='sqlite3')
    converter_options = ConverterOptions('', '')
    reader.open(storage_options, converter_options)

    # Get the list of topics and their types
    topic_types = reader.get_all_topics_and_types()
    topics = {topic.name: topic.type for topic in topic_types}
    print(f"Topics found: {topics}")

    # Prepare the CSV file
    with open(output_csv, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Collect headers
        headers = ['timestamp']
        for topic, msg_type in topics.items():
            msg_fields = get_message(msg_type).get_fields_and_field_types().keys()
            headers += [f"{topic.replace('/', '_')}_{field}" for field in msg_fields]

        writer.writerow(headers)

        # Process messages and write them to the CSV
        while reader.has_next():
            (topic, data, timestamp) = reader.read_next()
            msg_type = topics[topic]
            msg = deserialize_message(data, get_message(msg_type))

            # Prepare a single row with timestamp and all topic data
            row = [timestamp]
            for other_topic, other_msg_type in topics.items():
                if topic == other_topic:
                    row += [getattr(msg, field) for field in msg.__slots__]
                else:
                    # Fill with empty values for other topics
                    row += [''] * len(get_message(other_msg_type).get_fields_and_field_types())

            writer.writerow(row)

    print(f"Data extracted to: {output_csv}")


if __name__ == '__main__':
    # Path to your ROS 2 bag file
    bag_path = '/home/adishree/turtlebot3_ws/my_bag_file'

    # Path to the output CSV file
    output_csv = '/home/adishree/turtlebot3_ws/src/topics2.csv'

    # Extract and save data
    extract_rosbag2_to_single_csv(bag_path, output_csv)
