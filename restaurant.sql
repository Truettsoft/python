-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Oct 15, 2024 at 07:23 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `restaurant`
--

-- --------------------------------------------------------

--
-- Table structure for table `category`
--

CREATE TABLE `category` (
  `id` int(150) NOT NULL,
  `category_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `category`
--

INSERT INTO `category` (`id`, `category_name`) VALUES
(1, 'Appetizers'),
(2, 'Entrees'),
(3, 'Sides'),
(4, 'Beverages'),
(5, 'Desserts'),
(6, 'Kids Menu'),
(7, 'Drinks'),
(8, 'Special Dietary Needs');

-- --------------------------------------------------------

--
-- Table structure for table `employee`
--

CREATE TABLE `employee` (
  `id` int(50) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(100) NOT NULL,
  `username` varchar(150) NOT NULL,
  `password` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `employee`
--

INSERT INTO `employee` (`id`, `name`, `email`, `phone`, `username`, `password`) VALUES
(1, 'chithra', 'chithra@gmail.com', '1234567890', 'chithra', '123'),
(2, 'devi', 'devi@gmail.com', '9087654321', 'devi', '123'),
(3, 'chithradevi', 'sfds@gmail.com', '8790654321', 'chithradevi', '123'),
(4, 'varshi', 'varshi@gmail.com', '7890654321', 'varshi', '123'),
(5, 'siva', 'siva@gmail.com', '5678904321', 'siva', '123'),
(6, 'devii', 'hfg@gmail.com', '9632584107', 'devi', 'devi@123'),
(7, 'Dhanashika', 'dhanashika@gamil.com', '9632584107', 'dhanu', '@123'),
(8, 'dhanu', 'dhanashika@gamil.com', '9632584107', 'dhanu', 'dhanu@123'),
(9, 'subha', 'dhanashika@gamil.com', '9632584107', 'subha', '123'),
(10, 'priya', 'dhanashika@gamil.com', '8520369741', 'priya', '123'),
(11, 'dharshini', 'dhanashika@gamil.com', '9632584107', 'dharshini', '123');

-- --------------------------------------------------------

--
-- Table structure for table `menu`
--

CREATE TABLE `menu` (
  `id` int(150) NOT NULL,
  `category` varchar(255) NOT NULL,
  `menu_name` varchar(100) NOT NULL,
  `description` varchar(1000) NOT NULL,
  `price` varchar(150) NOT NULL,
  `image` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `menu`
--

INSERT INTO `menu` (`id`, `category`, `menu_name`, `description`, `price`, `image`) VALUES
(1, 'Appetizers', ' spring rolls', 'ddertet', '1', 'rolls.jpeg'),
(2, 'Appetizers', 'Mushroom Burger', 'sfsfs', '200', 'burger.jpg'),
(3, 'Entrees', 'Crispy Fried Chicken', 'dfgdd', '250', 'fried-chicken.jpg'),
(4, 'Entrees', 'Grilled chicken', 'sdsfsf', '350', 'grilled_chicken.jpg'),
(5, 'Entrees', 'Finger fish', 'sdfs', '150', 'finger-fish.jpg'),
(6, 'Appetizers', 'Meatballs', 'asdad', '100', 'meat.jpeg'),
(7, 'Desserts', 'Gulabjamun', 'fdsfds', '100', 'gulabjamun.jpg'),
(8, 'Drinks', 'Mojito', 'adsad', '100', 'Mojito.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `order`
--

CREATE TABLE `order` (
  `id` int(150) NOT NULL,
  `firstname` varchar(255) NOT NULL,
  `lastname` varchar(255) NOT NULL,
  `phone` varchar(100) NOT NULL,
  `email` varchar(150) NOT NULL,
  `address` varchar(500) NOT NULL,
  `product` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` int(150) NOT NULL,
  `firstname` varchar(255) NOT NULL,
  `lastname` varchar(255) NOT NULL,
  `phone` varchar(100) NOT NULL,
  `email` varchar(1000) NOT NULL,
  `address` varchar(150) NOT NULL,
  `product` varchar(150) NOT NULL,
  `price` varchar(150) NOT NULL,
  `quantity` int(11) NOT NULL,
  `subtotal` varchar(150) NOT NULL,
  `unseen` tinyint(1) NOT NULL,
  `seen` tinyint(1) NOT NULL,
  `transaction_id` varchar(255) NOT NULL,
  `payer_id` varchar(255) NOT NULL,
  `payment_status` varchar(50) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `firstname`, `lastname`, `phone`, `email`, `address`, `product`, `price`, `quantity`, `subtotal`, `unseen`, `seen`, `transaction_id`, `payer_id`, `payment_status`, `created_at`) VALUES
(1, 'chithra', 'devi', '1234567890', 'devi@gmail.com', 'wrewrrew', ' spring rolls', '100', 2, '200', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(2, 'devi', 'chintu', '2147483645', 'devi..@gmail.com', 'vhghhg', ' spring rolls', '100', 1, '100', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(3, 'devi', 'chintu', '2147483645', 'devi..@gmail.com', 'vhghhg', 'Mushroom Burger', '200', 1, '200', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(4, 'devi', 'chithra', '9876543210', 'sfds@gmail.com', 'vhghhg', ' spring rolls', '100', 1, '100', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(5, 'devi', 'chithra', '9876543210', 'sfds@gmail.com', 'vhghhg', 'Mushroom Burger', '200', 1, '200', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(6, 'devi', 'chithra', '9876543210', 'sfds@gmail.com', 'vhghhg', ' spring rolls, Mushroom Burger, Crispy Fried Chicken', '250', 1, '250', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(7, 'chintu', 'chithra', '2147483646', 'admin@gmail.com', 'vhghhg', 'Mojito', '100', 1, '100', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(8, 'chintu', 'chithra', '2147483646', 'admin@gmail.com', 'vhghhg', 'Gulabjamun', '100', 1, '100', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(9, 'chintu', 'chithra', '2147483646', 'admin@gmail.com', 'vhghhg', 'Meatballs', '100', 1, '100', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(10, 'chintu', 'chithra', '2147483646', 'admin@gmail.com', 'vhghhg', 'Mojito, Gulabjamun, Meatballs, Finger fish', '150', 1, '150', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(11, 'varshi', 'chithra', '9434567890', 'devi@gmail.com', 'vhghhg', ' spring rolls (1 x 100.0),Mushroom Burger (1 x 200.0)', '300', 2, '300', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(12, 'chintu', 'varshi', '2147483645', 'admin@gmail.com', 'vhghhgqw', 'Crispy Fried Chicken', '350', 2, '350', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(13, 'devi', 'chithra', '2147483646', 'admin@gmail.com', 'vhghhgqw', 'Grilled chicken', '600', 2, '600', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(15, 'chintu', 'varshi', '2147483645', 'sfds@gmail.com', 'vhghhg', 'Mushroom Burger, Meatballs', '300', 2, '300', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(16, 'banu', 'Dhanashika', '9632584107', 'dhanashika@gamil.com', 'gvhnvgbgn', ' spring rolls', '200', 2, '200', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(17, 'chithra', 'Dhanashika', '9632584107', 'dhanashika@gamil.com', 'gvhnvgbgn', ' spring rolls', '100', 1, '100', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(18, 'chithradevi', 'Dhanashika', '9632584107', 'dhanashika@gamil.com', 'gvhnvgbgn', 'Mushroom Burger', '400', 2, '400', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(19, 'chithra', 'Dhanashika', '91 9842095703', 'dhanashika@gamil.com', 'gvhnvgbgn', 'Mushroom Burger', '400', 2, '400', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(20, 'banu', 'Dhanashika', '9632584107', 'dhanashika@gamil.com', 'gvhnvgbgn', ' spring rolls, Mushroom Burger', '300', 2, '300', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(21, 'sivakami', 'Dhanashika', '3698521470', 'dhanashika@gamil.com', 'gvhnvgbgn', ' spring rolls', '200', 2, '200', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(22, 'banu', 'Dhanashika', '9856320147', 'dhanashika@gamil.com', 'gvhnvgbgn', 'Crispy Fried Chicken', '250', 1, '250', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(23, 'chithra', 'devi', '9632584107', 'devi@gmail.com', 'gvhnvgbgn', ' spring rolls, Mushroom Burger, Crispy Fried Chicken, Gulabjamun', '850', 6, '850', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(26, 'devi', 'Dhanashika', '9632584107', 'dhanashika@gamil.com', 'gvhnvgbgn', 'Mushroom Burger,  spring rolls', '300', 2, '300', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(27, 'banu', 'Dhanashika', '9632584107', 'dhanashika@gamil.com', 'gvhnvgbgn', 'Crispy Fried Chicken, Mushroom Burger', '450', 2, '450', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(28, 'banu', 'Dhanashika', '9632584107', 'dhanashika@gamil.com', 'gvhnvgbgn', 'Crispy Fried Chicken, Mushroom Burger,  spring rolls', '550', 3, '550', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(30, 'banu', 'Dhanashika', '8520369741', 'dhanashika@gamil.com', 'gvhnvgbgn', 'Mushroom Burger,  spring rolls, Meatballs', '400', 3, '400', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(31, 'chithra', 'Dhanashika', '91 9842095703', 'dhanashika@gamil.com', 'gvhnvgbgn', ' spring rolls, Meatballs', '200', 2, '200', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(32, 'chithradevi', 'Dhanashika', '9632584107', 'dhanashika@gamil.com', 'gvhnvgbgn', ' spring rolls, Mushroom Burger, Meatballs, Finger fish', '550', 4, '550', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(33, 'devi', 'Dhanashika', '8520369741', 'dhanashika@gamil.com', 'gvhnvgbgn', ' spring rolls, Mushroom Burger, Gulabjamun, Mojito, Finger fish', '650', 5, '650', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(34, 'devi', 'Dhanashika', '8520369741', 'dhanashika@gamil.com', 'gvhnvgbgn', ' spring rolls, Mushroom Burger, Gulabjamun, Mojito, Finger fish, Crispy Fried Chicken', '900', 6, '900', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(35, 'devi', 'Dhanashika', '8520369741', 'dhanashika@gamil.com', 'gvhnvgbgn', ' spring rolls, Mushroom Burger, Gulabjamun, Mojito, Finger fish, Crispy Fried Chicken', '900', 6, '900', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(36, 'chithra', 'Dhanashika', '3698521470', 'dhanashika@gamil.com', 'gvhnvgbgn', ' spring rolls, Mushroom Burger, Crispy Fried Chicken', '550', 3, '550', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(37, 'sivakami', 'Dhanashika', '9632584107', 'dhanashika@gamil.com', 'gvhnvgbgn', ' spring rolls, Mushroom Burger', '300', 2, '300', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(38, 'kasthu', 'Dhanashika', '9632584107', 'dhanashika@gamil.com', 'gvhnvgbgn', ' spring rolls, Mushroom Burger', '300', 2, '300', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(39, 'chithra', 'Dhanashika', '9856320147', 'dhanashika@gamil.com', 'gvhnvgbgn', 'Mushroom Burger,  spring rolls', '300', 2, '300', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(40, 'chithra', 'Dhanashika', '9632584107', 'dhanashika@gamil.com', 'gvhnvgbgn', ' spring rolls, Mushroom Burger', '300', 2, '300', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(41, 'chithra', 'Dhanashika', '9632584107', 'dhanashika@gamil.com', 'gvhnvgbgn', ' spring rolls, Mushroom Burger', '300', 2, '300', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(42, 'devi', 'Dhanashika', '3698521470', 'dhanashika@gamil.com', 'gvhnvgbgn', ' spring rolls', '100', 1, '100', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(43, 'chithra', 'Dhanashika', '3698521470', 'dhanashika@gamil.com', 'gvhnvgbgn', ' spring rolls', '100', 1, '100', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(44, 'banu', 'Dhanashika', '9856320147', 'dhanashika@gamil.com', 'gvhnvgbgn', ' spring rolls, Mushroom Burger', '300', 2, '300', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(45, 'banu', 'Dhanashika', '9856320147', 'dhanashika@gamil.com', 'gvhnvgbgn', ' spring rolls, Mushroom Burger', '300', 2, '300', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(46, 'chithradevi', 'Dhanashika', '3698521470', 'dhanashika@gamil.com', 'gvhnvgbgn', ' spring rolls, Mushroom Burger', '300', 2, '300', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(47, 'devi', 'Dhanashika', '91 9842095703', 'dhanashika@gamil.com', 'gvhnvgbgn', ' spring rolls, Crispy Fried Chicken', '350', 2, '350', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(48, 'banu', 'Dhanashika', '8520369741', 'dhanashika@gamil.com', 'gvhnvgbgn', 'Finger fish', '150', 1, '150', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(49, 'chithra', 'Dhanashika', '9632584107', 'dhanashika@gamil.com', 'gvhnvgbgn', ' spring rolls, Mushroom Burger', '300', 2, '300', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(50, 'chithra', 'Dhanashika', '9632584107', 'dhanashika@gamil.com', 'gvhnvgbgn', ' spring rolls, Mushroom Burger, Crispy Fried Chicken', '550', 3, '550', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(51, 'chithra', 'Dhanashika', '9856320147', 'dhanashika@gamil.com', 'gvhnvgbgn', ' spring rolls', '10000', 100, '10000', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(52, 'chithradevi', 'Dhanashika', '9632584107', 'dhanashika@gamil.com', 'gvhnvgbgn', ' spring rolls, Mushroom Burger', '300', 2, '300', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(53, 'chithra', 'Dhanashika', '9632584107', 'dhanashika@gamil.com', 'gvhnvgbgn', ' spring rolls, Mushroom Burger', '500', 3, '500', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(54, 'sfg', 'f', '4235345', 'sddf@gmail.com', 'try', ' spring rolls, Mushroom Burger', '300', 2, '300', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(55, 'sfg', 'sdfsdf', '34243543', 'sddf@gmail.com', 'ghfgh', ' spring rolls', '100', 1, '100', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(56, 'sfgsd', 'sfdf', '123-45-678', 'tsittutorial@gmail.com', 'ghfgh', ' spring rolls, Mushroom Burger', '300', 2, '300', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(57, 'sfgsd', 'sdfsdf', '34243543', 'sddf@gmail.com', 'ghfgh', ' spring rolls, Mushroom Burger', '300', 2, '300', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(58, 'sfgsd', 'sdfsdf', '34243543', 'sddf@gmail.com', 'ghfgh', ' spring rolls, Mushroom Burger, Crispy Fried Chicken', '550', 3, '550', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(59, 'sfgsd', 'sdfsdf', '1234567890', 'chithradevi.bchain@gmail.com', 'try', 'Mushroom Burger', '200', 1, '200', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(60, 'sfgsd', 'sdfsdf', '6545652412', 'sb-vd5qq31450937@personal.example.com', 'ghfgh', 'Mushroom Burger', '200', 1, '200', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(61, 'chithra', 'Dhanashika', '9632584107', 'dhanashika@gamil.com', 'gvhnvgbgn', ' spring rolls', '100', 1, '100', 0, 1, '', '', '', '2024-07-12 05:49:40'),
(64, 'chithra', 'Dhanashika', '9632584107', 'dhanashika@gamil.com', 'gvhnvgbgn', ' spring rolls', '1', 1, '1', 0, 1, '', '', '', '2024-07-12 06:05:17'),
(65, 'chithradevi', 'Dhanashika', '9632584107', 'dhanashika@gamil.com', 'gvhnvgbgn', ' spring rolls', '1', 1, '1', 0, 1, '42F425430A950733S', 'BQ7Q8NRBEL96S', 'COMPLETED', '2024-07-12 06:12:53'),
(66, 'chithra', 'Dhanashika', '9632584107', 'dhanashika@gamil.com', 'gvhnvgbgn', ' spring rolls', '1', 1, '1', 0, 1, '1BJ892194N653031C', 'BQ7Q8NRBEL96S', 'COMPLETED', '2024-07-12 06:26:16');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `category`
--
ALTER TABLE `category`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `employee`
--
ALTER TABLE `employee`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `menu`
--
ALTER TABLE `menu`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `order`
--
ALTER TABLE `order`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `category`
--
ALTER TABLE `category`
  MODIFY `id` int(150) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `employee`
--
ALTER TABLE `employee`
  MODIFY `id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `menu`
--
ALTER TABLE `menu`
  MODIFY `id` int(150) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `order`
--
ALTER TABLE `order`
  MODIFY `id` int(150) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(150) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=67;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
