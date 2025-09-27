-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: ecommee
-- ------------------------------------------------------
-- Server version	8.0.42

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admindata`
--

DROP TABLE IF EXISTS `admindata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admindata` (
  `adminid` int unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `phone_no` varchar(20) DEFAULT NULL,
  `email` varchar(50) NOT NULL,
  `password` varbinary(255) DEFAULT NULL,
  `agreed` enum('on','off') DEFAULT NULL,
  `address` varchar(50) DEFAULT NULL,
  `profile_img` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`adminid`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `phone_no` (`phone_no`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admindata`
--

LOCK TABLES `admindata` WRITE;
/*!40000 ALTER TABLE `admindata` DISABLE KEYS */;
INSERT INTO `admindata` VALUES (2,'Srikanth lak','2959959544','lakshmisrikanth2004@gmail.com',_binary '$2b$12$5asEscFd/RRjlaMLuB9IduITD0XT0iA2yDSWxdP3NyBvHdmqPWLYG','on','satya','B6uF0a.jpg');
/*!40000 ALTER TABLE `admindata` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `items`
--

DROP TABLE IF EXISTS `items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `items` (
  `item_id` binary(16) NOT NULL,
  `item_name` text NOT NULL,
  `item_description` longtext,
  `price` decimal(20,4) DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  `category` enum('Home appliances','electronics','fashion','sports','grocery') DEFAULT NULL,
  `item_image` varchar(15) DEFAULT NULL,
  `added_by` int unsigned DEFAULT NULL,
  PRIMARY KEY (`item_id`),
  KEY `added_by` (`added_by`),
  CONSTRAINT `items_ibfk_1` FOREIGN KEY (`added_by`) REFERENCES `admindata` (`adminid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `items`
--

LOCK TABLES `items` WRITE;
/*!40000 ALTER TABLE `items` DISABLE KEYS */;
INSERT INTO `items` VALUES (_binary '!�Ԕx\��80\�B&e ','Godrej aer Matic Kit (Machine + 1 Refill) - Automatic Room Fresheners with Flexi Control Spray | Violet Valley Bloom | 2200 Sprays Guaranteed | Lasts up to 60 days (210ml)','Scent	violet valley bloom\r\nColour	Violet Valley Bloom\r\nBrand	Godrej aer\r\nItem Form	Spray\r\nItem dimensions L x W x H	11.6 x 9 x 23 Centimeters',451.0000,1,'Home appliances','L8hO6h.jpg',2),(_binary 'HnG�z\��80\�B&e ','Popular Willow Cricket Bat with Tennis Ball M Size 4 (8-10 Year) with Ball Pack of 1, Wood','\r\nSize	8-10 Year\r\nSport	Cricket\r\nBrand	Generic\r\nMaterial	Wood\r\nColour	Multicolored',600.0000,1,'sports','K2iP5r.jpg',2),(_binary '����w\��80\�B&e ','Tata Salt 1 Kg, Free Flowing and Iodised Namak, Vacuum Evaporated, Salt in Fresh','\r\nFlavour	Iodised Salt\r\nBrand	TATA SALT\r\nItem Weight	1 Kilograms\r\nSpeciality	Vegetarian\r\nNet Quantity	1000.0 gram',30.0000,1,'grocery','O0wW1p.jpg',2),(_binary '�]�\��80\�B&e ','kjh','oiuy',987.0000,98765,'grocery','V5kF8p.jpg',2),(_binary '):*��\��80\�B&e ','jh','lkjhg vbnm,',222.0000,1,'Home appliances','Y0fR3k.jpg',2),(_binary '9�@\�z\��80\�B&e ','Visit the Boldfit Store Boldfit Gym T-Shirts for Men – Premium Polyester Sports Tshirt with Moisture-Wicking, Breathable Fabric & Regular Fit for Running, Workout & Activewear for Man','Material compositionPolyester\r\nPatternSolid\r\nFit typeRegular Fit\r\nSleeve typeHalf Sleeve\r\nCollar styleCrew Neck\r\nLengthStandard Length\r\nCountry of OriginIndia',500.0000,80,'sports','U0xO2v.jpg',2),(_binary 'f�j�\��80\�B&e ','ooooo','lkjhc',200.0000,1,'fashion','J4eY0g.',2),(_binary 'v�\�Ҕw\��80\�B&e ','Surf Excel Easy Wash Detergent Powder - 1500 G','About this item\r\nSURF EXCEL EASY WASH DETERGENT POWDER: This detergent targets tough stains with its superfine powder and removes them easily without being harsh on the fabric. So, enjoy your dinner parties and let go of the fear of stains — your clothes will be blemish-free and bright as before with this detergent.\r\n100% STAIN REMOVAL: This superfine detergent powder makes the tedious job of washing clothes easier. This washing powder will remove all stains — from ketchup stains, mud blemishes, and food spills to paint spots — with ease and leave your clothes fresh and spotless.\r\nCOLOUR CARE: Our Surf Excel Washing Powder gets rid of stubborn stains but retains the original colour of the fabric. It works on both coloured and white clothes and ensures that the colour does not transfer and your clothes do not become dull.\r\nEASY AND BETTER DISSOLUTION: The Surf Excel Easy Wash detergent powder dissolves very quickly in water. It also reaches the stains on the clothes effortlessly without leaving any residue on the clothes or the washing machine.\r\nPOWER OF 10 HANDS: The engineered formula and superior technology of Surf Excel Easy Wash Washing Powder unleashes the power of 10 hands that effectively removes even the most stubborn stains, be it oil, curry, dirt, etc.\r\nHow to Use: To hand-wash clothes, use 2 scoops of Surf excel Easy Wash detergent powder. For machine-wash, use 3 scoops of Surf Excel Easy Wash washing powder. For tough stains, pre-soak your clothes in Surf Excel Easy Wash solution for 30 mins.\r\n',50.0000,1,'grocery','H7bB6a.jpg',2),(_binary 'v�x\��80\�B&e ','Lymio Men Cargo || Men Cargo Pants Cotton || Casual Cargos Pant (Cargo-46-49)','Material typeCotton\r\nLengthLong Length\r\nStyleCargo\r\nClosure typeDrawstring\r\nOccasion typeCasual\r\nCare instructionsMachine Wash\r\nCountry of OriginIndia',900.0000,1,'fashion','X1rE0k.jpg',2),(_binary '���x\��80\�B&e ','OLEVS Stainless Steel Luxury Analogue Men\'S Watch(Green-Gold Dial & Silver & Gold Colored Strap)-Ol85G','Case diameter30 Centimetres\r\nBand colourGold\r\nBand material typeStainless Steel\r\nWarranty type1 Year on manufacturing defects\r\nWatch movement typeQuartz\r\nCase thickness11 Millimetres\r\nCountry of OriginHong Kong',30000.0000,1,'fashion','N9uY1o.jpg',2),(_binary '\�M�f�y\��80\�B&e ','Amazon Basics Hard Shell EVA Headphone Carrying Case for Universal Oversized Over-Ear Headset, Shockproof, Water Repellent, Anti-Pressure Portable Protective Pouch/Storage Bag, Black','\r\nBrand	amazon basics\r\nColour	Black - Hard Shell EVA\r\nCompatible Devices	Headphones\r\nForm Factor	Case\r\nShell Type	Hard',600.0000,1,'Home appliances','X6fC8f.jpg',2),(_binary '\��q�x\��80\�B&e ','Sony WH-CH520 Wireless Bluetooth Headphones On Ear with Mic, Up to 50Hrs Battery, Quick Charge, DSEE Upscale, Multipoint Connectivity, Voice Assistant, Customized EQ-Black','\r\nBrand	Sony\r\nColour	Black\r\nEar Placement	On Ear\r\nForm Factor	On Ear\r\nImpedance	100 Ohm',4900.0000,1,'electronics','M1mF8a.jpg',2),(_binary '\�_�ٔw\��80\�B&e ','Qlect Portable Blender Electric Juicers Fruit Mixers USB Rechargeable Smoothie Mini Personal Juicer 6 Blades 3Gears With 1500 Mah Rechargeable Battery-Smoothie Blender','Portable Blender with 𝐄𝐱𝐭𝐫𝐚 𝐋𝐢𝐝】 -This hand blender for kitchen has the design of 1500𝐦𝐚𝐡 𝐫𝐞𝐜𝐡𝐚𝐫𝐠𝐞𝐚𝐛𝐥𝐞 𝐛𝐚𝐭𝐭𝐞𝐫𝐲, and 𝐫𝐞𝐦𝐨𝐯𝐚𝐛𝐥𝐞 𝐛𝐚𝐬𝐞.Compact design and perfect size for a personal blender without taking up much space, lightweight for on-the-go, work, travelling and gym use.This electric blender can best act as small juicer for fruits or mini juicer for fruits.\r\n【Powerful and 6 Blades Mixer Grinder or Vegetable Juicer Machine 】-The powerful Mini blender for shakes and smoothies is not only equipped with a 𝟐𝟐,𝟎𝟎𝟎𝐫𝐩𝐦 𝐬𝐩𝐞𝐞𝐝 45𝐖 𝐦𝐨𝐭𝐨𝐫, but also built in 1𝟔𝐩𝐜𝐬 𝐮𝐥𝐭𝐫𝐚-𝐬𝐡𝐚𝐫𝐩 𝟑𝟎𝟒 𝐬𝐭𝐚𝐢𝐧𝐥𝐞𝐬𝐬 𝐬𝐭𝐞𝐞𝐥 𝐛𝐥𝐚𝐝𝐞𝐬, convenient for making quick breakfast smoothies and meal replacements, particulaly healthy smoothies and personal juicing.\r\n【𝗟𝗮𝗿𝗴𝗲 𝗖𝗮𝗽𝗮𝗰𝗶𝘁𝘆 𝗮𝗻𝗱 𝗦𝗲𝗹𝗳-𝗰𝗹𝗲𝗮𝗻𝗶𝗻𝗴 Juice Maker 】-This blender for smoothies has large capacity of 50𝟎𝐦𝐥. Add 80% water, double click to clean automatically.The 𝐢𝐧𝐜𝐥𝐮𝐝𝐞𝐝 𝐜𝐥𝐞𝐚𝐧𝐢𝐧𝐠 𝐛𝐫𝐮𝐬𝐡 is used for fine clean, no need to worry about not cleaning properly.This electric juicer for fruits is also known as portable juicer blender, juice machine, juicer machine electric all fruits or juice maker machine for fruits.\r\n【Upgrade 𝐒𝐞𝐜𝐮𝐫𝐢𝐭𝐲 𝐅𝐞𝐚𝐭𝐮𝐫𝐞𝐬 of Juicer Machine handy 】-This small blender mixer for shakes and smoothies ',900.0000,1,'Home appliances','Z1dH7l.jpg',2);
/*!40000 ALTER TABLE `items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `order_id` binary(30) NOT NULL,
  `item_id` binary(16) DEFAULT NULL,
  `item_name` longtext,
  `quantity` int unsigned DEFAULT NULL,
  `total_amount` decimal(20,4) DEFAULT NULL,
  `order_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `item_image` varchar(20) DEFAULT NULL,
  `payment_by` int unsigned DEFAULT NULL,
  PRIMARY KEY (`order_id`),
  KEY `payment_by` (`payment_by`),
  KEY `item_id` (`item_id`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`payment_by`) REFERENCES `userdata` (`userid`) ON DELETE SET NULL,
  CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`item_id`) REFERENCES `items` (`item_id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (_binary 'order_RLPby9GyRv9qVa\0\0\0\0\0\0\0\0\0\0',_binary 'HnG�z\��80\�B&e ','Popular Willow Cricket Bat with Tennis Ball M Size 4 (8-10 Year) with Ball Pack of 1, Wood',1,60000.0000,'2025-09-24 16:23:57','K2iP5r.jpg',1),(_binary 'order_RLPffRN1TsmhtD\0\0\0\0\0\0\0\0\0\0',_binary '���x\��80\�B&e ','OLEVS Stainless Steel Luxury Analogue Men\'S Watch(Green-Gold Dial & Silver & Gold Colored Strap)-Ol85G',1,3000000.0000,'2025-09-24 16:25:22','N9uY1o.jpg',1),(_binary 'order_RLPh5LTbzCWMvy\0\0\0\0\0\0\0\0\0\0',_binary '\��q�x\��80\�B&e ','Sony WH-CH520 Wireless Bluetooth Headphones On Ear with Mic, Up to 50Hrs Battery, Quick Charge, DSEE Upscale, Multipoint Connectivity, Voice Assistant, Customized EQ-Black',1,490000.0000,'2025-09-24 16:26:47','M1mF8a.jpg',1);
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews`
--

DROP TABLE IF EXISTS `reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews` (
  `review_id` int unsigned NOT NULL AUTO_INCREMENT,
  `review_text` text,
  `rating` enum('1','2','3','4','5') DEFAULT NULL,
  `item_id` binary(16) DEFAULT NULL,
  `user_id` int unsigned DEFAULT NULL,
  `comment_at` datetime DEFAULT CURRENT_TIMESTAMP,
  `review_title` text,
  PRIMARY KEY (`review_id`),
  KEY `item_id` (`item_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `reviews_ibfk_1` FOREIGN KEY (`item_id`) REFERENCES `items` (`item_id`) ON DELETE SET NULL,
  CONSTRAINT `reviews_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `userdata` (`userid`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews`
--

LOCK TABLES `reviews` WRITE;
/*!40000 ALTER TABLE `reviews` DISABLE KEYS */;
INSERT INTO `reviews` VALUES (1,'fghjk','3',_binary '!�Ԕx\��80\�B&e ',1,'2025-09-27 15:24:10','fghjkl');
/*!40000 ALTER TABLE `reviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userdata`
--

DROP TABLE IF EXISTS `userdata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `userdata` (
  `userid` int unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(30) NOT NULL,
  `phone_no` varchar(10) DEFAULT NULL,
  `address` text,
  `usergender` enum('male','female') DEFAULT NULL,
  `useremail` varchar(50) NOT NULL,
  `password` varbinary(255) NOT NULL,
  PRIMARY KEY (`userid`),
  UNIQUE KEY `useremail` (`useremail`),
  UNIQUE KEY `phone_no` (`phone_no`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userdata`
--

LOCK TABLES `userdata` WRITE;
/*!40000 ALTER TABLE `userdata` DISABLE KEYS */;
INSERT INTO `userdata` VALUES (1,'lakshmi srikanth ','8978218784','satyanaryana puram vijayawada','male','lakshmisrikanth2004@gmail.com',_binary '$2b$12$wsdmBDJqvPrx68k7fEnpP.W5p/F9Yssg0qWYiwGI/AtNGZ35TC.c6');
/*!40000 ALTER TABLE `userdata` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-09-27 16:00:05
