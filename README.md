# Smart Home Energy Management System (SHEMS) 

##  Introduction:
The Smart Home Energy Management System (SHEMS) plays an important role in empowering homeowners to take control of their energy consumption and optimize electricity expenses. In this database design, we present a comprehensive and normalized relational schema that forms the backbone of SHEMS. The following schema design encapsulates the core entities and relationships needed to store and manage information related to service locations, enrolled devices, device events, and energy prices.

Key elements of the schema include a User table to store user details, a ServiceLocation table to manage multiple locations per user, a DeviceModel table to store predefined device types and models, an EnrolledDevice table to track specific instances of devices enrolled by users, an EventData table to capture events and energy consumption data generated by devices, and an EnergyPrices table to store hourly energy prices based on location.

This relational database schema aims to facilitate the implementation of SHEMS, enabling users to explore their historical energy usage patterns, make informed decisions to optimize energy consumption, and reduce energy costs. 



## ER Diagram:
As part of the design process, we have created an ER Diagram that will be translated into a relational database schema.
<img width="827" alt="Screenshot 2024-02-15 at 6 10 47 PM" src="https://github.com/rishienandhan3/dbmsSHEMS/assets/143848239/a87f4ff3-113c-4460-919a-9ca51a6fbb9c">

## Relational Schema:
- User (UserID, AddressID, first_name, last_name, email, phone)
- ServiceLocation (LocationID, UserID, AddressID, move_in_date, square_footage, bedrooms, occupants)
- Address (AddressID, type, unit, street, house_num, city, state, zip)
- DeviceModel (ModelID, model_type, model_number, other_details)
- EnrolledDevice (DeviceID, LocationID, ModelID) 
- EventData (EventID, DeviceID, event_type, label, value, event_time)
- EnergyPrice (hourly_price, price_time, zip)

## Assumptions and cardinalities for relationships:
- We assume a one-to-many relationship between User and ServiceLocation as a user can own multiple locations but a location can be owned only by a single user
- Each service location can only be present in one address and hence we model the present_in relationship set as one-to-one relationship
- We assume a one-to-many relationship between Address and EnergyPrice as multiple addresses which are present in the same zip code can have the same hourly prices but not vice-versa 
- The relationship set existing between EventData and EnergyPrice can be modeled as a one-to-many relationship as multiple events reported by devices in the same hour will have the same hourly price but each event can be associated with a single hourly price
- Each EnrolledDevice can generate multiple EventData and multiple devices can generate the same type of event data. So we model the ‘generates’ relationship set as many-to-many relationship
- Each unique device can only be enrolled in one service location but each location can have multiple devices enrolled. So ‘present_in’ relationship set can be modeled as one-to-many relationship
- Each EnrolledDevice is of a specific Model type and multiple devices can be of the same model type. So, we model the ‘of_type’ relationship set as one-to-many relationship
- Each user has a unique billing address and hence we assume a one-to-one relationship for the ‘billing_address’ relationship set

## Foreign key relationships:
- User.AddressID is the foreign key reference to Address.AddressID
- ServiceLocation.UserID is the foreign key reference to User.UserID
- ServiceLocation.AddressID is the foreign key reference to Address.AddressID
- EnrolledDevice.LocationID is the foreign key reference to ServiceLocation.LocationID
- EnrolledDevice.ModelID is the foreign key reference to DeviceModel.ModelID
- EventData.DeviceID is the foreign key reference to EnrolledDevice.DeviceID
- EnergyPrice.price_time is the foreign key reference to EventData.event_time
- EnergyPrice.zip is the foreign key reference to Address.zip

## Key considerations:
- The schema is normalized to reduce data redundancy and improve data integrity. For example, the DeviceModel table separates the device type and model details to avoid repeating the same information for devices of the same model
- It is assumed that there is a predefined list of device types and models in the DeviceModel table, and users choose from this list when enrolling devices
- The schema assumes smart devices send data to the SHEMS database automatically, and there's no need to model the process of data transmission
- The schema assumes that the types of events and corresponding values are predefined in the device model
- Energy prices are assumed to change hourly, and the EnergyPrices table allows for storing prices for different hours and locations
- Prices can be retrieved based on the timestamp and location for calculating energy costs
- The schema aims to be space-efficient by avoiding redundant information and maintaining relationships through keys
- This schema provides a foundation for storing information about customers, their service locations, enrolled devices, and device data. It supports the tracking of energy usage, events, and energy prices over time. Depending on the specific requirements of querying and reporting for the web interface (which we would be building on Project-2), additional adjustments or optimizations may be necessary

## Summary:
- Designed and developed a module for a Smart Home Energy Management System (SHEMS) focusing on storing and managing past energy usage data, enabling users to comprehend their energy consumption and costs related to various appliances and settings.

- Implemented user account management features, allowing customers to sign up, add multiple service locations with detailed information, and enroll smart devices such as AC, dryer, lights, and refrigerator, capturing essential data like model number, type, and events.

- Developed a robust data storage system for SHEMS, handling diverse types of information sent by enrolled devices, including events (switching on/off, setting changes) and energy consumption data, ensuring accurate recording with device ID, time stamp, event label, and corresponding values.

- Integrated functionality to capture and store dynamic energy prices, considering hourly variations and location-dependent fluctuations based on zip codes, enhancing the system's capability to calculate energy costs accurately over time.

- Created web-based UI with measures to guard against SQL injection, cross-site scripting attacks and concurrent access, allowing users to optimize their energy consumption using impactful data summaries and visualization. 

