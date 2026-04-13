CREATE DATABASE  IF NOT EXISTS `artemis_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `artemis_db`;
-- MySQL dump 10.13  Distrib 8.0.45, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: artemis_db
-- ------------------------------------------------------
-- Server version	8.0.45

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add controlo',1,'add_controlo'),(2,'Can change controlo',1,'change_controlo'),(3,'Can delete controlo',1,'delete_controlo'),(4,'Can view controlo',1,'view_controlo'),(5,'Can add equipas',2,'add_equipas'),(6,'Can change equipas',2,'change_equipas'),(7,'Can delete equipas',2,'delete_equipas'),(8,'Can view equipas',2,'view_equipas'),(9,'Can add f documents',3,'add_fdocuments'),(10,'Can change f documents',3,'change_fdocuments'),(11,'Can delete f documents',3,'delete_fdocuments'),(12,'Can view f documents',3,'view_fdocuments'),(13,'Can add funcionarios',4,'add_funcionarios'),(14,'Can change funcionarios',4,'change_funcionarios'),(15,'Can delete funcionarios',4,'delete_funcionarios'),(16,'Can view funcionarios',4,'view_funcionarios'),(17,'Can add membros equipas',5,'add_membrosequipas'),(18,'Can change membros equipas',5,'change_membrosequipas'),(19,'Can delete membros equipas',5,'delete_membrosequipas'),(20,'Can view membros equipas',5,'view_membrosequipas'),(21,'Can add cargos',6,'add_cargos'),(22,'Can change cargos',6,'change_cargos'),(23,'Can delete cargos',6,'delete_cargos'),(24,'Can view cargos',6,'view_cargos'),(25,'Can add departamentos',7,'add_departamentos'),(26,'Can change departamentos',7,'change_departamentos'),(27,'Can delete departamentos',7,'delete_departamentos'),(28,'Can view departamentos',7,'view_departamentos'),(29,'Can add users',8,'add_users'),(30,'Can change users',8,'change_users'),(31,'Can delete users',8,'delete_users'),(32,'Can view users',8,'view_users'),(33,'Can add log entry',9,'add_logentry'),(34,'Can change log entry',9,'change_logentry'),(35,'Can delete log entry',9,'delete_logentry'),(36,'Can view log entry',9,'view_logentry'),(37,'Can add permission',10,'add_permission'),(38,'Can change permission',10,'change_permission'),(39,'Can delete permission',10,'delete_permission'),(40,'Can view permission',10,'view_permission'),(41,'Can add group',11,'add_group'),(42,'Can change group',11,'change_group'),(43,'Can delete group',11,'delete_group'),(44,'Can view group',11,'view_group'),(45,'Can add content type',12,'add_contenttype'),(46,'Can change content type',12,'change_contenttype'),(47,'Can delete content type',12,'delete_contenttype'),(48,'Can view content type',12,'view_contenttype'),(49,'Can add session',13,'add_session'),(50,'Can change session',13,'change_session'),(51,'Can delete session',13,'delete_session'),(52,'Can view session',13,'view_session'),(53,'Can add Vaga',14,'add_vaga'),(54,'Can change Vaga',14,'change_vaga'),(55,'Can delete Vaga',14,'delete_vaga'),(56,'Can view Vaga',14,'view_vaga'),(57,'Can add Candidato',15,'add_candidatos'),(58,'Can change Candidato',15,'change_candidatos'),(59,'Can delete Candidato',15,'delete_candidatos'),(60,'Can view Candidato',15,'view_candidatos'),(61,'Can add Processo Seletivo',16,'add_processoseletivo'),(62,'Can change Processo Seletivo',16,'change_processoseletivo'),(63,'Can delete Processo Seletivo',16,'delete_processoseletivo'),(64,'Can view Processo Seletivo',16,'view_processoseletivo'),(65,'Can add Planeamento de Férias',17,'add_planamentferias'),(66,'Can change Planeamento de Férias',17,'change_planamentferias'),(67,'Can delete Planeamento de Férias',17,'delete_planamentferias'),(68,'Can view Planeamento de Férias',17,'view_planamentferias'),(69,'Can add Conversa Cronos',18,'add_conversacronos'),(70,'Can change Conversa Cronos',18,'change_conversacronos'),(71,'Can delete Conversa Cronos',18,'delete_conversacronos'),(72,'Can view Conversa Cronos',18,'view_conversacronos'),(73,'Can add Mensagem Cronos',19,'add_mensagemcronos'),(74,'Can change Mensagem Cronos',19,'change_mensagemcronos'),(75,'Can delete Mensagem Cronos',19,'delete_mensagemcronos'),(76,'Can view Mensagem Cronos',19,'view_mensagemcronos'),(77,'Can add produto',20,'add_produto'),(78,'Can change produto',20,'change_produto'),(79,'Can delete produto',20,'delete_produto'),(80,'Can view produto',20,'view_produto'),(81,'Can add categoria',21,'add_categoria'),(82,'Can change categoria',21,'change_categoria'),(83,'Can delete categoria',21,'delete_categoria'),(84,'Can view categoria',21,'view_categoria'),(85,'Can add fornecedor',22,'add_fornecedor'),(86,'Can change fornecedor',22,'change_fornecedor'),(87,'Can delete fornecedor',22,'delete_fornecedor'),(88,'Can view fornecedor',22,'view_fornecedor'),(89,'Can add movimentacao',23,'add_movimentacao'),(90,'Can change movimentacao',23,'change_movimentacao'),(91,'Can delete movimentacao',23,'delete_movimentacao'),(92,'Can view movimentacao',23,'view_movimentacao'),(93,'Can add Relatório Agendado',24,'add_relatorioagendado'),(94,'Can change Relatório Agendado',24,'change_relatorioagendado'),(95,'Can delete Relatório Agendado',24,'delete_relatorioagendado'),(96,'Can view Relatório Agendado',24,'view_relatorioagendado'),(97,'Can add Relatório Gerado',25,'add_relatoriogerado'),(98,'Can change Relatório Gerado',25,'change_relatoriogerado'),(99,'Can delete Relatório Gerado',25,'delete_relatoriogerado'),(100,'Can view Relatório Gerado',25,'view_relatoriogerado');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `candidatos`
--

DROP TABLE IF EXISTS `candidatos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `candidatos` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nome` varchar(50) NOT NULL,
  `email` varchar(254) NOT NULL,
  `telefone` varchar(9) NOT NULL,
  `nacionalidade` varchar(45) NOT NULL,
  `cv` varchar(100) DEFAULT NULL,
  `estado` varchar(20) NOT NULL,
  `data_candidatura` datetime(6) NOT NULL,
  `vaga_id` bigint NOT NULL,
  `nota` longtext NOT NULL,
  `fonte_recrutamento` varchar(69) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `candidatos_vaga_id_9e9a6f1f_fk_vagas_id` (`vaga_id`),
  CONSTRAINT `candidatos_vaga_id_9e9a6f1f_fk_vagas_id` FOREIGN KEY (`vaga_id`) REFERENCES `vagas` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `candidatos`
--

LOCK TABLES `candidatos` WRITE;
/*!40000 ALTER TABLE `candidatos` DISABLE KEYS */;
INSERT INTO `candidatos` VALUES (1,'Alberto Freguesias','albertofreguesias@gmail.com','922268651','angolana','','rejeitado','2026-03-15 16:56:33.819445',1,'1','linkedin'),(2,'Dimilneia Catihe','dimilneiacatihe@gmail.com','925547863','angolana','','rejeitado','2026-03-17 23:54:42.825473',3,'5','linkedin'),(3,'José Francisco','josefrancisco@gmail.com','964875123','angolana','','rejeitado','2026-03-18 00:09:46.979744',4,'5','linkedin'),(4,'George Washington Jr.','thisniggatripping@gmail.com','951753456','angolana','','rejeitado','2026-03-18 00:14:22.948297',4,'5','linkedin'),(5,'Edmar Leonardo','edmarleonardo@gmail.com','941250605','angolana','Vlad15.pdf','recebido','2026-03-18 10:50:28.243209',2,'Ele até sabe capinar. Isso é bastante importante.','candidatura_livre'),(6,'Rosa Malheiros','rosamalheiros@gmailcom','987654321','filipina','PAP_2026_Proposta (1).pdf','recebido','2026-03-18 11:09:43.238399',3,'A kota é Boa..','linkedin'),(7,'Maria Madalena','mariamadalena@gmail.com','916454888','angolana','Relatório de Estágio .pdf','oferta','2026-03-18 11:13:17.970433',4,'Ele é Bom','linkedin'),(8,'João Silva','joaosilva@gmail.com','908788541','angolana','','recebido','2026-03-19 10:01:14.910624',3,'Ele é... interessante','portal_recrutamento'),(9,'Ana silva','ana@gmail.com','900876543','angolana','','recebido','2026-03-19 10:02:29.550825',2,'Ela é bomba, ela é muito bomba','linkedin'),(10,'António Francisco','mantony@gmail.com','987333444','angolana','','recebido','2026-03-19 10:36:06.093398',1,'A','linkedin'),(11,'Ana Gomes','anita@gmail.com','911222333','angolana','','recebido','2026-03-19 10:36:06.160940',1,'a','linkedin');
/*!40000 ALTER TABLE `candidatos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cargos`
--

DROP TABLE IF EXISTS `cargos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cargos` (
  `id_cargo` int NOT NULL AUTO_INCREMENT,
  `nome_cargo` varchar(45) NOT NULL,
  `descricao` text NOT NULL,
  `requisitos` text NOT NULL,
  `sal_min` decimal(10,2) unsigned zerofill NOT NULL,
  `sal_base` decimal(10,2) NOT NULL,
  `sal_max` decimal(10,2) NOT NULL,
  `data_criacao` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `ativo` tinyint NOT NULL DEFAULT '1',
  PRIMARY KEY (`id_cargo`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cargos`
--

LOCK TABLES `cargos` WRITE;
/*!40000 ALTER TABLE `cargos` DISABLE KEYS */;
INSERT INTO `cargos` VALUES (1,'Gerente de Produção','Responsável por supervisionar toda a produção agrícola de laranjas, desde o plantio até a colheita','Formação em Agronomia ou áreas afins, 5+ anos de experiência em gestão agrícola',01500000.00,1750000.00,2000000.00,'2025-01-09 23:00:00',1),(2,'Supervisor Agrícola','Coordena as equipes de campo e monitora o desenvolvimento dos pomares','Formação técnica em Agricultura, 3+ anos de experiência em fruticultura',00450000.00,550000.00,700000.00,'2025-01-11 23:00:00',1),(3,'Técnico em Irrigação','Responsável pela manutenção e operação dos sistemas de irrigação dos pomares','Curso técnico em irrigação, conhecimentos em sistemas de irrigação por gotejamento',00250000.00,350000.00,450000.00,'2025-01-14 23:00:00',1),(4,'Operador de Colheita','Opera máquinas e equipamentos especializados na colheita de laranjas','Carteira de habilitação categoria C, experiência com máquinas agrícolas',00180000.00,250000.00,350000.00,'2025-01-17 23:00:00',1),(5,'Controlador de Pragas','Monitora e controla pragas e doenças nos pomares de laranja','Formação em Agronomia ou técnica em Defesa Sanitária Vegetal',00300000.00,400000.00,500000.00,'2025-01-19 23:00:00',1),(6,'Armazenista Frigorífico','Responsável pelo armazenamento refrigerado e conservação pós-colheita','Conhecimentos em refrigeração industrial, cuidados pós-colheita',00220000.00,300000.00,400000.00,'2025-01-21 23:00:00',1),(7,'Gestor de Qualidade','Garante a qualidade dos frutos conforme padrões de mercado e exportação','Formação em Engenharia de Alimentos ou Agronomia, certificação em qualidade',00600000.00,800000.00,1000000.00,'2025-01-24 23:00:00',1),(8,'Operário Agrícola','Executa atividades manuais nos pomares (poda, adubação, limpeza)','Ensino fundamental completo, resistência física para trabalho ao ar livre',00080000.00,120000.00,180000.00,'2025-01-27 23:00:00',1),(9,'Técnico em Fertilidade do Solo','Analisa solos e recomenda correções e adubações para os pomares','Formação em Agronomia com especialização em solos',00350000.00,450000.00,600000.00,'2025-01-31 23:00:00',1),(10,'Assistente Administrativo','Responsável pela documentação, controle de produção e apoio administrativo','Formação em Administração ou contabilidade, domínio de informática',00025000.00,100000.00,180000.00,'2025-02-02 23:00:00',1);
/*!40000 ALTER TABLE `cargos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `controlo`
--

DROP TABLE IF EXISTS `controlo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `controlo` (
  `id_controlo` int NOT NULL AUTO_INCREMENT,
  `numero_faltas` int NOT NULL,
  `numero_presencas` int NOT NULL,
  `inicio_carreira` date NOT NULL,
  `fim_carreira` date DEFAULT NULL,
  `dias_acomulados` int NOT NULL,
  `dias_disponiveis` int NOT NULL,
  `dias_ferias` int NOT NULL,
  `f_id` int DEFAULT NULL,
  `direito_ferias_anual` int NOT NULL,
  `ferias_gozadas` int NOT NULL,
  `ferias_agendadas` int NOT NULL,
  `ferias_restantes` int NOT NULL,
  `baixa_medica_dias` int NOT NULL,
  `licenca_maternidade_dias` int NOT NULL,
  `licenca_sem_vencimento_dias` int NOT NULL,
  `ferias_vencidas` int NOT NULL,
  `ultimo_ano_ferias` int NOT NULL,
  PRIMARY KEY (`id_controlo`),
  KEY `controlo_f_id_062992a4_fk_funcionarios_f_id` (`f_id`),
  CONSTRAINT `controlo_f_id_062992a4_fk_funcionarios_f_id` FOREIGN KEY (`f_id`) REFERENCES `funcionarios` (`f_id`)
) ENGINE=InnoDB AUTO_INCREMENT=105 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `controlo`
--

LOCK TABLES `controlo` WRITE;
/*!40000 ALTER TABLE `controlo` DISABLE KEYS */;
INSERT INTO `controlo` VALUES (1,0,0,'2025-11-04',NULL,0,22,22,15,22,0,0,22,0,0,0,0,2026),(2,0,0,'2025-05-22',NULL,0,22,22,17,22,0,0,22,0,0,0,0,2026),(3,0,0,'2024-08-31',NULL,0,22,22,23,22,0,0,22,0,0,0,0,2026),(4,0,0,'2025-03-31',NULL,0,22,22,25,22,0,0,22,0,0,0,0,2026),(5,0,0,'2024-01-27',NULL,0,22,22,27,22,0,0,22,0,0,0,0,2026),(6,0,0,'2025-02-26',NULL,0,22,22,28,22,0,0,22,0,0,0,0,2026),(7,0,0,'2025-03-01',NULL,0,22,22,29,22,0,0,22,0,0,0,0,2026),(8,0,0,'2024-02-26',NULL,0,22,22,30,22,0,0,22,0,0,0,0,2026),(9,0,0,'2024-01-15',NULL,0,22,22,36,22,0,0,22,0,0,0,0,2026),(10,0,0,'2021-05-17',NULL,0,22,22,38,22,0,0,22,0,0,0,0,2026),(11,0,0,'2021-12-01',NULL,0,22,22,42,22,0,0,22,0,0,0,0,2026),(12,0,0,'2020-10-05',NULL,0,22,22,45,22,0,0,22,0,0,0,0,2026),(13,0,0,'2021-07-11',NULL,0,22,22,48,22,0,0,22,0,0,0,0,2026),(14,0,0,'2021-08-14',NULL,0,22,22,52,22,0,0,22,0,0,0,0,2026),(15,0,0,'2023-10-02',NULL,0,22,22,53,22,0,0,22,0,0,0,0,2026),(16,0,0,'2025-01-20',NULL,0,22,22,55,22,0,0,22,0,0,0,0,2026),(17,0,0,'2021-11-08',NULL,0,22,22,56,22,0,0,22,0,0,0,0,2026),(18,0,0,'2022-07-29',NULL,0,22,22,58,22,0,0,22,0,0,0,0,2026),(19,0,0,'2022-02-25',NULL,0,22,22,60,22,0,0,22,0,0,0,0,2026),(20,0,0,'2024-07-08',NULL,0,22,22,66,22,0,0,22,0,0,0,0,2026),(21,0,0,'2023-02-28',NULL,0,22,22,67,22,0,0,22,0,0,0,0,2026),(22,0,0,'2023-11-07',NULL,0,22,22,75,22,1,15,6,0,0,0,0,2026),(23,0,0,'2022-05-03',NULL,0,22,22,76,22,0,0,22,0,0,0,0,2026),(24,0,0,'2022-09-07',NULL,0,22,22,91,22,0,0,22,0,0,0,0,2026),(25,0,0,'2025-03-01',NULL,0,22,22,94,22,0,0,22,0,0,0,0,2026),(26,0,0,'2023-07-04',NULL,0,22,22,95,22,0,0,22,0,0,0,0,2026),(27,0,0,'2020-09-25',NULL,0,22,22,96,22,0,0,22,0,0,0,0,2026),(28,0,0,'2021-07-22',NULL,0,22,22,98,22,0,0,22,0,0,0,0,2026),(29,0,0,'2023-10-31',NULL,0,22,22,99,22,0,0,22,0,0,0,0,2026),(30,0,0,'2026-03-26',NULL,0,22,22,101,22,6,0,16,0,0,0,0,2026),(31,0,0,'2026-03-29',NULL,0,22,22,103,22,0,0,22,0,0,0,0,2026),(32,0,0,'2024-05-06',NULL,0,22,22,1,22,0,0,22,0,0,0,0,0),(33,0,0,'2024-01-22',NULL,0,22,22,2,22,0,0,22,0,0,0,0,0),(34,0,0,'2025-01-18',NULL,0,22,22,3,22,0,0,22,0,0,0,0,0),(35,0,0,'2024-07-16',NULL,0,22,22,4,22,0,0,22,0,0,0,0,0),(36,0,0,'2024-07-05',NULL,0,22,22,5,22,0,0,22,0,0,0,0,0),(37,0,0,'2024-12-08',NULL,0,22,22,6,22,0,0,22,0,0,0,0,0),(38,0,0,'2024-12-14',NULL,0,22,22,7,22,0,0,22,0,0,0,0,0),(39,0,0,'2025-12-15',NULL,0,22,22,8,22,0,0,22,0,0,0,0,0),(40,0,0,'2024-04-26',NULL,0,22,22,9,22,0,0,22,0,0,0,0,0),(41,0,0,'2024-02-16',NULL,0,22,22,10,22,0,0,22,0,0,0,0,0),(42,0,0,'2025-11-16',NULL,0,22,22,11,22,0,0,22,0,0,0,0,0),(43,0,0,'2024-03-18',NULL,0,22,22,12,22,0,0,22,0,0,0,0,0),(44,0,0,'2026-01-10',NULL,0,22,22,13,22,0,0,22,0,0,0,0,0),(45,0,0,'2024-09-14',NULL,0,22,22,14,22,0,0,22,0,0,0,0,0),(46,0,0,'2024-07-03',NULL,0,22,22,16,22,0,0,22,0,0,0,0,0),(47,0,0,'2025-01-13',NULL,0,22,22,18,22,0,0,22,0,0,0,0,0),(48,0,0,'2025-01-03',NULL,0,22,22,19,22,0,0,22,0,0,0,0,0),(49,0,0,'2025-12-07',NULL,0,22,22,20,22,0,0,22,0,0,0,0,0),(50,0,0,'2024-01-19',NULL,0,22,22,21,22,0,0,22,0,0,0,0,0),(51,0,0,'2025-01-15',NULL,0,22,22,22,22,0,0,22,0,0,0,0,0),(52,0,0,'2024-03-17',NULL,0,22,22,24,22,0,0,22,0,0,0,0,0),(53,0,0,'2025-03-14',NULL,0,22,22,26,22,0,0,22,0,0,0,0,0),(54,0,0,'2025-09-05',NULL,0,22,22,31,22,0,0,22,0,0,0,0,0),(55,0,0,'2026-03-31',NULL,0,22,22,32,22,0,0,22,0,0,0,0,0),(56,0,0,'2023-03-10',NULL,0,22,22,33,22,0,0,22,0,0,0,0,0),(57,0,0,'2022-11-05',NULL,0,22,22,34,22,0,0,22,0,0,0,0,0),(58,0,0,'2023-06-20',NULL,0,22,22,35,22,0,0,22,0,0,0,0,0),(59,0,0,'2022-08-22',NULL,0,22,22,37,22,0,0,22,0,0,0,0,0),(60,0,0,'2024-09-01',NULL,0,22,22,39,22,0,0,22,0,0,0,0,0),(61,0,0,'2022-03-14',NULL,0,22,22,40,22,0,0,22,0,0,0,0,0),(62,0,0,'2023-07-28',NULL,0,22,22,41,22,0,0,22,0,0,0,0,0),(63,0,0,'2022-06-18',NULL,0,22,22,43,22,0,0,22,0,0,0,0,0),(64,0,0,'2025-02-10',NULL,0,22,22,44,22,0,0,22,0,0,0,0,0),(65,0,0,'2023-04-22',NULL,0,22,22,46,22,0,0,22,0,0,0,0,0),(66,0,0,'2022-09-30',NULL,0,22,22,47,22,0,0,22,0,0,0,0,0),(67,0,0,'2023-01-19',NULL,0,22,22,49,22,0,0,22,0,0,0,0,0),(68,0,0,'2024-11-07',NULL,0,22,22,50,22,0,0,22,0,0,0,0,0),(69,0,0,'2022-05-23',NULL,0,22,22,51,22,0,0,22,0,0,0,0,0),(70,0,0,'2022-04-16',NULL,0,22,22,54,22,0,0,22,0,0,0,0,0),(71,0,0,'2023-08-15',NULL,0,22,22,57,22,0,0,22,0,0,0,0,0),(72,0,0,'2020-12-03',NULL,0,22,22,59,22,0,0,22,0,0,0,0,0),(73,0,0,'2025-03-05',NULL,0,22,22,61,22,0,0,22,0,0,0,0,0),(74,0,0,'2021-06-17',NULL,0,22,22,62,22,0,0,22,0,0,0,0,0),(75,0,0,'2023-05-11',NULL,0,22,22,63,22,0,0,22,0,0,0,0,0),(76,0,0,'2021-09-22',NULL,0,22,22,64,22,0,0,22,0,0,0,0,0),(77,0,0,'2022-10-14',NULL,0,22,22,65,22,0,0,22,0,0,0,0,0),(78,0,0,'2021-04-06',NULL,0,22,22,68,22,0,0,22,0,0,0,0,0),(79,0,0,'2022-12-19',NULL,0,22,22,69,22,0,0,22,0,0,0,0,0),(80,0,0,'2020-07-31',NULL,0,22,22,70,22,0,0,22,0,0,0,0,0),(81,0,0,'2023-09-16',NULL,0,22,22,71,22,0,0,22,0,0,0,0,0),(82,0,0,'2025-02-28',NULL,0,22,22,72,22,0,0,22,0,0,0,0,0),(83,0,0,'2022-01-10',NULL,0,22,22,73,22,0,0,22,0,0,0,0,0),(84,0,0,'2021-10-24',NULL,0,22,22,74,22,0,0,22,0,0,0,0,0),(85,0,0,'2023-03-25',NULL,0,22,22,77,22,0,0,22,0,0,0,0,0),(86,0,0,'2024-08-19',NULL,0,22,22,78,22,0,0,22,0,0,0,0,0),(87,0,0,'2021-02-08',NULL,0,22,22,79,22,0,0,22,0,0,0,0,0),(88,0,0,'2022-08-31',NULL,0,22,22,80,22,0,0,22,0,0,0,0,0),(89,0,0,'2023-06-14',NULL,0,22,22,81,22,0,0,22,0,0,0,0,0),(90,0,0,'2020-11-29',NULL,0,22,22,82,22,0,0,22,0,0,0,0,0),(91,0,0,'2025-01-06',NULL,0,22,22,83,22,0,0,22,0,0,0,0,0),(92,0,0,'2022-07-12',NULL,0,22,22,84,22,0,0,22,0,0,0,0,0),(93,0,0,'2021-03-17',NULL,0,22,22,85,22,0,0,22,0,0,0,0,0),(94,0,0,'2021-08-03',NULL,0,22,22,86,22,0,0,22,0,0,0,0,0),(95,0,0,'2023-04-09',NULL,0,22,22,87,22,0,0,22,0,0,0,0,0),(96,0,0,'2022-11-21',NULL,0,22,22,88,22,0,0,22,0,0,0,0,0),(97,0,0,'2021-05-28',NULL,0,22,22,89,22,0,0,22,0,0,0,0,0),(98,0,0,'2024-10-15',NULL,0,22,22,90,22,0,0,22,0,0,0,0,0),(99,0,0,'2023-12-18',NULL,0,22,22,92,22,0,0,22,0,0,0,0,0),(100,0,0,'2021-01-13',NULL,0,22,22,93,22,0,0,22,0,0,0,0,0),(101,0,0,'2022-04-07',NULL,0,22,22,97,22,0,0,22,0,0,0,0,0),(102,0,0,'2022-06-09',NULL,0,22,22,100,22,0,0,22,0,0,0,0,0),(103,0,0,'2026-04-01',NULL,0,22,22,104,22,0,0,22,0,0,0,0,2026);
/*!40000 ALTER TABLE `controlo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cronos_conversas`
--

DROP TABLE IF EXISTS `cronos_conversas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cronos_conversas` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `titulo` varchar(200) NOT NULL,
  `resumo` longtext,
  `data_inicio` datetime(6) NOT NULL,
  `data_fim` datetime(6) DEFAULT NULL,
  `ativa` tinyint(1) NOT NULL,
  `num_mensagens` int NOT NULL,
  `usuario_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `cronos_conv_usuario_b82cb4_idx` (`usuario_id`,`data_inicio` DESC),
  KEY `cronos_conv_ativa_c0ce1c_idx` (`ativa`),
  CONSTRAINT `cronos_conversas_usuario_id_883cf9a3_fk_users_id` FOREIGN KEY (`usuario_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cronos_conversas`
--

LOCK TABLES `cronos_conversas` WRITE;
/*!40000 ALTER TABLE `cronos_conversas` DISABLE KEYS */;
INSERT INTO `cronos_conversas` VALUES (1,'Conversa luisgonzaga@gmail.com',NULL,'2026-04-02 17:24:17.836787','2026-04-02 17:30:41.402661',0,0,3),(2,'Conversa luisgonzaga@gmail.com',NULL,'2026-04-02 17:30:48.678402','2026-04-02 17:30:50.612966',0,0,3),(3,'Conversa luisgonzaga@gmail.com',NULL,'2026-04-03 12:46:52.044682',NULL,1,14,3),(4,'Conversa gylmiguel07@gmail.com',NULL,'2026-04-08 15:44:27.732014','2026-04-12 16:20:08.902427',0,0,1),(5,'Conversa alcides@dev.com',NULL,'2026-04-11 09:43:16.849989',NULL,1,12,2),(6,'Conversa waldirenylua@gmail.com',NULL,'2026-04-11 13:13:34.583866',NULL,1,0,5),(7,'Conversa gylmiguel07@gmail.com',NULL,'2026-04-12 16:20:14.217481',NULL,1,4,1);
/*!40000 ALTER TABLE `cronos_conversas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cronos_mensagens`
--

DROP TABLE IF EXISTS `cronos_mensagens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cronos_mensagens` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `tipo` varchar(10) NOT NULL,
  `conteudo` longtext NOT NULL,
  `tipo_resposta` varchar(10) NOT NULL,
  `sql_gerado` longtext,
  `resultado_sql` longtext,
  `data_criacao` datetime(6) NOT NULL,
  `tokens_utilizados` int NOT NULL,
  `conversa_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `cronos_mens_convers_0e1887_idx` (`conversa_id`,`data_criacao`),
  KEY `cronos_mens_tipo_5e9988_idx` (`tipo`),
  CONSTRAINT `cronos_mensagens_conversa_id_eb8e9a3e_fk_cronos_conversas_id` FOREIGN KEY (`conversa_id`) REFERENCES `cronos_conversas` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cronos_mensagens`
--

LOCK TABLES `cronos_mensagens` WRITE;
/*!40000 ALTER TABLE `cronos_mensagens` DISABLE KEYS */;
INSERT INTO `cronos_mensagens` VALUES (1,'user','Olá','text',NULL,NULL,'2026-04-11 09:43:21.575884',0,5),(2,'assistant','Olá! Eu sou o **CRONOS**, o teu assistente de inteligência artificial integrado ao ERP Artemis.\n\nEstou aqui para te ajudar a consultar e analisar os dados da empresa de forma rápida e eficiente. Posso gerar relatórios sobre funcionários, departamentos, cargos ou qualquer outra informação presente no nosso banco de dados.\n\nComo posso ajudar-te hoje?','sql',NULL,NULL,'2026-04-11 09:43:21.602475',0,5),(3,'user','gere um relatório do rh','text',NULL,NULL,'2026-04-11 09:43:53.338823',0,5),(4,'assistant','## Relatório Geral de Recursos Humanos\n\n**Resumo executivo:** A organização conta actualmente com um quadro de **103 colaboradores** distribuídos por 20 departamentos especializados, evidenciando uma estrutura operacional robusta e diversificada.\n\n### Distribuição por Departamento\nA força de trabalho está distribuída de forma equilibrada, com um foco ligeiramente superior nas actividades operacionais e de controlo.\n\n| Departamento | Total de Funcionários | % do Total |\n| :--- | :---: | :---: |\n| **Operações de Campo** | 8 | 7.8% |\n| **Controlo de Pragas e Doenças** | 7 | 6.8% |\n| **Controlo de Qualidade** | 7 | 6.8% |\n| **Laboratório de Análise** | 7 | 6.8% |\n| **Pós-colheita e Armazenamento** | 7 | 6.8% |\n| **Compras e Suprimentos** | 6 | 5.8% |\n| **Logística e Distribuição** | 6 | 5.8% |\n| **Gestão de Recursos Hídricos** | 5 | 4.9% |\n| **Pesquisa e Desenvolvimento** | 5 | 4.9% |\n| **Produção Agrícola** | 5 | 4.9% |\n| **Recursos Humanos** | 5 | 4.9% |\n| **Sustentabilidade Ambiental** | 5 | 4.9% |\n| **Tecnologia da Informação** | 5 | 4.9% |\n| **Administração e Secretariado** | 4 | 3.9% |\n| **Departamento Financeiro** | 4 | 3.9% |\n| **Manutenção de Equipamentos** | 4 | 3.9% |\n| **Vendas e Marketing** | 4 | 3.9% |\n| **Direção Geral** | 3 | 2.9% |\n| **Relações Institucionais** | 3 | 2.9% |\n| **Segurança e Saúde Ocupacional** | 3 | 2.9% |\n\n---\n\n### Análise e Recomendações\n- **Foco Operacional:** Existe uma concentração significativa de pessoal em áreas críticas de produção e qualidade (Operações de Campo, Controlo de Pragas, Qualidade e Laboratório), o que demonstra uma orientação para a excelência do produto final.\n- **Estrutura de Suporte:** Os departamentos de suporte (TI, RH, Financeiro) mantêm dimensões adequadas para a gestão de um efectivo de 103 pessoas, garantindo a sustentabilidade administrativa.\n- **Especialização:** A presença de departamentos como Sustentabilidade Ambiental e Gestão de Recursos Hídricos indica um compromisso da empresa com práticas modernas e responsáveis.\n\n---\n> **Quer explorar mais?**\n> 1. Posso listar os nomes e cargos dos funcionários de um departamento específico?\n> 2. Gostaria de ver a análise salarial média por cada um destes departamentos?\n> 3. Deseja identificar quem são os supervisores e responsáveis por cada área?','sql',NULL,NULL,'2026-04-11 09:43:53.346692',0,5),(5,'user','Gera um relatório completo de capital humano com análise salarial por departamento e gráfico de distribuição','text',NULL,NULL,'2026-04-11 10:26:37.437097',0,5),(6,'assistant','## Relatório de Capital Humano e Análise Salarial\n\n**Resumo executivo:** De momento, não foi possível gerar a análise detalhada pois não existem dados de funcionários ativos ou associações de departamentos registadas no sistema.\n\n### Estado da Base de Dados\nApós a consulta ao banco de dados do ERP Artemis, verificou-se que não existem registos que cruzem as informações de **Funcionários**, **Cargos** e **Departamentos** para os critérios solicitados. Isto pode dever-se a:\n- Inexistência de funcionários marcados como \"Ativos\".\n- Falta de associação entre os funcionários e os seus respetivos departamentos ou cargos.\n- Tabelas de salários base nos cargos ainda não preenchidas.\n\n---\n\n### Análise e Recomendações\n- **Validação de Cadastros:** Recomenda-se verificar no módulo de RH se os funcionários estão devidamente vinculados a um departamento e se o campo \"Ativo\" está preenchido corretamente.\n- **Configuração de Cargos:** É essencial que cada cargo tenha os valores de salário base definidos para que o cálculo da massa salarial seja possível.\n- **Sincronização:** Caso os dados tenham sido inseridos recentemente, certifique-se de que a base de dados foi atualizada.\n\n---\n> **Quer explorar mais?**\n> 1. Posso listar todos os funcionários cadastrados para verificarmos o estado de cada um?\n> 2. Deseja ver apenas a lista de departamentos e cargos existentes para validar as configurações?\n> 3. Posso verificar se existem funcionários sem departamento atribuído?','sql',NULL,NULL,'2026-04-11 10:26:37.444421',0,5),(7,'user','Quantos funcionários temos no total, distribuídos por sexo e estado civil? Inclui gráfico.','text',NULL,NULL,'2026-04-11 10:30:37.688391',0,5),(8,'assistant','## Relatório de Distribuição Demográfica de Funcionários\n\n**Resumo executivo:** A empresa conta atualmente com um total de **103 funcionários**, apresentando um equilíbrio de género notável e uma predominância de colaboradores solteiros.\n\n### Distribuição por Sexo e Estado Civil\nA tabela abaixo detalha a composição da nossa força de trabalho cruzando o género com o estado civil:\n\n| Sexo | Estado Civil | Total de Funcionários |\n| :--- | :--- | :--- |\n| **Feminino** | Solteira | 29 |\n| **Masculino** | Solteiro | 27 |\n| **Feminino** | Casada | 22 |\n| **Masculino** | Casado | 21 |\n| **Masculino** | Divorciado | 4 |\n\n---\n\n### Análise e Recomendações\n- **Equilíbrio de Género:** A força de trabalho está quase perfeitamente dividida, com **52 homens** e **51 mulheres**, o que reflete uma política de contratação inclusiva.\n- **Perfil Jovem/Independente:** Existe uma maioria de colaboradores solteiros (56 no total, representando cerca de 54% da empresa), o que pode sugerir uma força de trabalho mais jovem ou com maior mobilidade.\n- **Estabilidade Familiar:** Uma parcela significativa (43 funcionários) é casada, o que geralmente está associado a uma maior retenção e estabilidade a longo prazo.\n\n---\n> **Quer explorar mais?**\n> - Posso detalhar a distribuição destes funcionários por cada departamento?\n> - Queres ver a média de idades para cada um destes grupos?\n> - Posso gerar um relatório sobre a média salarial comparando homens e mulheres?','sql',NULL,NULL,'2026-04-11 10:30:37.698411',0,5),(9,'user','quem são os divorciados?','text',NULL,NULL,'2026-04-11 10:31:30.213404',0,5),(10,'assistant','## Relatório de Funcionários Divorciados\n\n**Resumo executivo:** Foram identificados **4 funcionários** com o estado civil \"Divorciado\", todos do sexo masculino e integrados em departamentos técnicos e operacionais da empresa.\n\n### Listagem de Colaboradores\nA tabela abaixo apresenta os detalhes dos funcionários identificados no sistema:\n\n| Nome Completo | Departamento | Cargo |\n| :--- | :--- | :--- |\n| **Ilídio Machado** | Manutenção de Equipamentos | Operário Agrícola |\n| **Umberto Fragoso** | Operações de Campo | Supervisor Agrícola |\n| **Nuno Borges** | Pós-colheita e Armazenamento | Técnico em Fertilidade do Solo |\n| **Hélder Queirós** | Laboratório de Análise | Técnico em Fertilidade do Solo |\n\n---\n\n### Análise e Recomendações\n- **Especialização Técnica:** Nota-se que este grupo é composto por profissionais de áreas críticas, com destaque para os dois Técnicos em Fertilidade do Solo, essenciais para a qualidade da produção.\n- **Distribuição Setorial:** Os colaboradores estão bem distribuídos por diferentes fases da operação, desde a manutenção e operações de campo até ao laboratório e pós-colheita.\n\n---\n> **Quer explorar mais?**\n> - Posso facultar os contactos telefónicos destes funcionários para fins administrativos?\n> - Deseja verificar o tempo de casa (data de contratação) de cada um deles?\n> - Gostaria de ver um relatório semelhante para outros estados civis (ex: Casados ou Viúvos)?','sql',NULL,NULL,'2026-04-11 10:31:30.220963',0,5),(11,'user','olá','text',NULL,NULL,'2026-04-11 12:49:11.848197',0,3),(12,'assistant','Olá! Eu sou o **CRONOS**, o teu assistente de inteligência artificial integrado ao ERP Artemis.\n\nEstou aqui para te ajudar a consultar e analisar todos os dados da empresa, desde informações sobre funcionários e departamentos até detalhes sobre cargos e utilizadores do sistema.\n\nComo posso ajudar-te hoje? Podes pedir-me, por exemplo:\n*   \"Faz um resumo dos funcionários por departamento.\"\n*   \"Quais são os cargos com os salários base mais altos?\"\n*   \"Lista os funcionários contratados este ano.\"\n*   \"Gera um relatório sobre a distribuição de género na empresa.\"\n\nDiz-me o que precisas e eu trato do resto!','sql',NULL,NULL,'2026-04-11 12:49:11.858226',0,3),(13,'user','quantos funcionários temos?','text',NULL,NULL,'2026-04-11 12:50:19.483106',0,3),(14,'assistant','## Relatório de Estado do Efetivo de Funcionários\n\n**Resumo executivo:** A empresa possui atualmente um total de **103 funcionários** registados no sistema, com **60 colaboradores em estado ativo**.\n\n### Distribuição por Situação Operacional\nA tabela abaixo detalha o estado atual de todos os colaboradores registados no ERP Artemis:\n\n| Estado | Total de Funcionários |\n| :--- | :---: |\n| **Ativo** | 60 |\n| **Afastado** | 41 |\n| **Férias** | 1 |\n| **Demitido** | 1 |\n| **Total Geral** | **103** |\n\n---\n\n### Análise e Recomendações\n- **Taxa de Atividade:** Aproximadamente **58%** do quadro de pessoal está atualmente ativo.\n- **Alerta de Afastamentos:** Observa-se um número elevado de funcionários na condição de **\"Afastado\" (41 colaboradores)**. É recomendável realizar uma auditoria interna para identificar os motivos (licenças médicas, licenças sem vencimento, etc.) e o impacto na produtividade dos departamentos afetados.\n- **Gestão de Férias:** Apenas 1 funcionário consta em gozo de férias no momento, o que pode sugerir uma concentração de férias em outros períodos ou necessidade de atualização do cronograma.\n\n---\n> **Quer explorar mais?**\n> - Posso listar quais são os funcionários que estão atualmente **afastados**?\n> - Gostaria de ver a distribuição destes funcionários por **departamento**?\n> - Quer saber quais cargos possuem o maior número de colaboradores **ativos**?','sql',NULL,NULL,'2026-04-11 12:50:19.490128',0,3),(15,'user','Quem foi o teu criador?','text',NULL,NULL,'2026-04-11 14:37:23.825882',0,5),(16,'assistant','Olá! Eu sou o **CRONOS**, a inteligência artificial nativa do **ERP Artemis**.\n\nFui desenvolvido pela equipa de engenharia e dados da **Artemis Softwares** para servir como o teu assistente inteligente na gestão empresarial. O meu propósito é facilitar o acesso à informação, realizar análises complexas de dados e ajudar-te a tomar decisões estratégicas com base nos dados reais da tua organização.\n\nComo posso ajudar-te com os dados da empresa hoje?','sql',NULL,NULL,'2026-04-11 14:37:23.832850',0,5),(17,'user','Mostra todos os cargos existentes com a respectiva faixa salarial mínima, base e máxima e gráfico de barras','text',NULL,NULL,'2026-04-11 14:56:12.934880',0,3),(18,'assistant','## Relatório de Estrutura Salarial por Cargo\n\n**Resumo executivo:** A estrutura salarial da empresa apresenta uma hierarquia clara, com o cargo de Gerente de Produção a liderar a tabela remuneratória, reflectindo uma amplitude salarial que vai desde os 100.000 Kz aos 1.750.000 Kz em termos de salário base.\n\n### Detalhe das Faixas Salariais\nA tabela abaixo apresenta os limites mínimos, a base de referência e os tectos máximos para cada função registada no sistema Artemis.\n\n| Cargo | Salário Mínimo (Kz) | Salário Base (Kz) | Salário Máximo (Kz) |\n| :--- | :---: | :---: | :---: |\n| **Gerente de Produção** | 1.500.000,00 | 1.750.000,00 | 2.000.000,00 |\n| **Gestor de Qualidade** | 600.000,00 | 800.000,00 | 1.000.000,00 |\n| **Supervisor Agrícola** | 450.000,00 | 550.000,00 | 700.000,00 |\n| **Técnico em Fertilidade do Solo** | 350.000,00 | 450.000,00 | 600.000,00 |\n| **Controlador de Pragas** | 300.000,00 | 400.000,00 | 500.000,00 |\n| **Técnico em Irrigação** | 250.000,00 | 350.000,00 | 450.000,00 |\n| **Armazenista Frigorífico** | 220.000,00 | 300.000,00 | 400.000,00 |\n| **Operador de Colheita** | 180.000,00 | 250.000,00 | 350.000,00 |\n| **Operário Agrícola** | 80.000,00 | 120.000,00 | 180.000,00 |\n| **Assistente Administrativo** | 25.000,00 | 100.000,00 | 180.000,00 |\n\n---\n\n### Análise e Recomendações\n- **Concentração de Valor:** O cargo de **Gerente de Produção** possui um salário base significativamente superior aos demais (mais do dobro do segundo cargo mais alto), o que indica uma elevada centralização de responsabilidade técnica e estratégica nesta função.\n- **Amplitude Salarial:** O cargo de **Assistente Administrativo** apresenta a maior variação proporcional entre o mínimo e o máximo, o que sugere uma política de progressão de carreira mais flexível ou a existência de diferentes níveis de senioridade dentro da mesma categoria.\n- **Equilíbrio Técnico:** Os cargos técnicos (Solo, Pragas, Irrigação) mantêm uma consistência salarial entre os 350.000 Kz e 450.000 Kz, facilitando a mobilidade interna ou ajustes por especialização.\n\n---\n> **Quer explorar mais?**\n> - Posso listar os funcionários que ocupam cada um destes cargos?\n> - Gostaria de ver o custo total da fol','sql',NULL,NULL,'2026-04-11 14:56:12.950403',0,3),(19,'user','Quantos funcionários temos no total, distribuídos por sexo e estado civil? Inclui gráfico.','text',NULL,NULL,'2026-04-11 14:57:27.993221',0,3),(20,'assistant','## Relatório de Distribuição de Funcionários por Sexo e Estado Civil\n\n**Resumo executivo:** A Artemis conta atualmente com um total de **103 funcionários**, apresentando uma distribuição equilibrada entre os géneros e uma predominância de colaboradores solteiros.\n\n### Distribuição Detalhada\nA tabela abaixo apresenta a segmentação dos colaboradores cruzando as variáveis de sexo e estado civil:\n\n| Sexo | Estado Civil | Total de Funcionários |\n| :--- | :--- | :--- |\n| Feminino | Casada | 22 |\n| Feminino | Solteira | 29 |\n| Masculino | Casado | 21 |\n| Masculino | Divorciado | 4 |\n| Masculino | Solteiro | 27 |\n\n---\n\n### Análise e Recomendações\n- **Equilíbrio de Género:** A força de trabalho está quase perfeitamente dividida, com **51 mulheres** e **52 homens**, o que reflete uma excelente paridade de género na organização.\n- **Predominância de Solteiros:** Cerca de **54%** da equipa é composta por solteiros (56 colaboradores), o que pode sugerir uma força de trabalho jovem ou com maior mobilidade.\n- **Estabilidade Familiar:** O grupo de colaboradores casados representa **42%** do total (43 colaboradores), um indicador positivo para a retenção de talentos a longo prazo.\n\n---\n> **Quer explorar mais?**\n> - Posso detalhar esta distribuição por **departamento** para identificar áreas mais jovens?\n> - Gostaria de ver a **média salarial** comparando colaboradores casados e solteiros?\n> - Quer saber qual é a **idade média** dos funcionários em cada uma destas categorias?','sql',NULL,NULL,'2026-04-11 14:57:28.003910',0,3),(21,'user','olá','text',NULL,NULL,'2026-04-12 16:20:48.893117',0,7),(22,'assistant','Olá! Eu sou o **CRONOS**, o teu assistente de inteligência artificial do ERP Artemis.\n\nEstou aqui para te ajudar a consultar e analisar todos os dados da empresa, desde informações sobre funcionários e departamentos até detalhes sobre cargos e salários.\n\nComo posso ajudar-te hoje? Podes pedir-me, por exemplo:\n*   \"Faz um resumo do quadro de pessoal por departamento.\"\n*   \"Quem são os funcionários que entraram este ano?\"\n*   \"Mostra-me a lista de cargos e as suas faixas salariais.\"\n*   \"Dá-me os detalhes do funcionário [Nome].\"\n\nDiz-me o que precisas e eu trato do resto!','sql',NULL,NULL,'2026-04-12 16:20:48.908999',0,7),(23,'user','você sabe o que é método  fifo(first in first out) em stock?','text',NULL,NULL,'2026-04-12 18:52:09.109136',0,7),(24,'assistant','Sim, compreendo perfeitamente o conceito. O método **FIFO** (do inglês *First In, First Out*), ou **PEPS** (Primeiro a Entrar, Primeiro a Sair), é um dos pilares da gestão de stocks e contabilidade logística.\n\nComo assistente do ERP Artemis, posso explicar-te como este método funciona e a sua importância:\n\n### O que é o Método FIFO?\nO princípio é simples: **os primeiros artigos a entrar no stock devem ser os primeiros a sair** (seja por venda ou para consumo interno). \n\n### Como funciona na prática:\n1.  **Cronologia:** O sistema regista a data e o custo de cada lote que entra no armazém.\n2.  **Saída de Mercadoria:** Quando ocorre uma venda, o sistema abate automaticamente as unidades do lote mais antigo disponível.\n3.  **Valorização:** O valor do stock que permanece em armazém é sempre composto pelos preços mais recentes, o que tende a reflectir melhor o valor de mercado actual.\n\n### Principais Vantagens:\n-   **Redução de Perdas:** É essencial para produtos perecíveis (alimentos, medicamentos) ou com prazos de validade, evitando que fiquem obsoletos no fundo da prateleira.\n-   **Fluxo de Caixa e Lucro:** Em períodos de inflação, o FIFO tende a apresentar um lucro bruto maior, pois o custo dos produtos vendidos é baseado em preços de compra mais antigos (e geralmente mais baixos).\n-   **Organização Logística:** Facilita a arrumação física do armazém, forçando a rotatividade dos produtos.\n\n---\n\n**Nota sobre o Sistema Artemis:**\nActualmente, o meu acesso directo ao banco de dados `artemis_db` está configurado para as tabelas de **Recursos Humanos** (Funcionários, Cargos, Departamentos e Utilizadores). Embora eu domine os conceitos de logística, para gerar relatórios de stock baseados em FIFO, seria necessário que as tabelas de inventário e movimentos de mercadoria fossem integradas ao meu esquema de consulta.\n\n---\n> **Quer explorar mais?**\n- Gostaria que eu explicasse a diferença entre o FIFO e o LIFO (Last In, First Out)?\n- Queres ver uma lista dos funcionários que pertencem ao departamento de Logística ou Armazém?\n- Posso ajudar a criar uma estrutura de cargos para a tua equipa de gestão de inventário?','sql',NULL,NULL,'2026-04-12 18:52:09.116467',0,7),(25,'user','Gera um relatório completo de capital humano com análise salarial por departamento e gráfico','text',NULL,NULL,'2026-04-13 04:49:07.165385',0,3),(26,'assistant','## Relatório de Capital Humano e Análise Salarial\n\n**Resumo executivo:** A estrutura salarial da exploração apresenta uma concentração de investimento nos departamentos de suporte logístico e relações institucionais, com o setor de Pós-colheita a representar a maior fatia da massa salarial total.\n\n### Distribuição Salarial por Departamento (Top 10)\nA tabela abaixo detalha os custos fixos com pessoal nos departamentos com maior impacto financeiro:\n\n| Departamento | Colaboradores | Massa Salarial (Kz) | Média Salarial (Kz) |\n| :--- | :---: | :---: | :---: |\n| **Pós-colheita e Armazenamento** | 4 | **3.450.000,00** | 862.500,00 |\n| **Relações Institucionais** | 3 | **2.550.000,00** | 850.000,00 |\n| **Pesquisa e Desenvolvimento** | 4 | **2.070.000,00** | 517.500,00 |\n| **Segurança e Saúde Ocupacional** | 2 | **2.000.000,00** | 1.000.000,00 |\n| **Laboratório de Análise** | 5 | **1.840.000,00** | 368.000,00 |\n| **Compras e Suprimentos** | 4 | **1.470.000,00** | 367.500,00 |\n| **Administração e Secretariado** | 3 | **1.450.000,00** | 483.333,33 |\n| **Controlo de Qualidade** | 3 | **1.400.000,00** | 466.666,67 |\n| **Manutenção de Equipamentos** | 3 | **1.320.000,00** | 440.000,00 |\n| **Operações de Campo** | 4 | **1.270.000,00** | 317.500,00 |\n\n---\n\n### Análise e Recomendações\n\n- **Especialização Técnica:** O departamento de **Segurança e Saúde Ocupacional** possui a maior média salarial (1.000.000,00 Kz), o que indica a presença de quadros altamente qualificados e essenciais para a conformidade legal da exploração.\n- **Foco Operacional:** O elevado investimento em **Pós-colheita e Armazenamento** demonstra que a empresa prioriza a preservação da qualidade da laranja após a colheita, garantindo o valor do produto final.\n- **Oportunidade de Revisão:** Departamentos como **Vendas e Marketing** e **Direção Geral** apresentam valores base muito baixos (120.000,00 Kz). Recomenda-se verificar se estes cargos estão devidamente enquadrados ou se necessitam de uma revisão na política de incentivos para retenção de talentos.\n- **Eficiência de Equipa:** O **Laboratório de Análise** é o departamento com mais colaboradores (5), mas mantém uma média salarial equilibrada, sugerindo uma estrutura de equipa com diferentes níveis de senioridade.\n\n---\n> **Quer explorar mais?**\n> 1. Deseja ver a lista detalhada de funcionários do departamento de Pós-colheita?\n> 2. Gostaria de comparar o desempenho (avaliação) com os salários actuais?\n> 3. Precisa de um resumo de custos apenas para os funcionários em regime \'eventual\'?','sql',NULL,NULL,'2026-04-13 04:49:07.184817',0,3),(27,'user','Mostra o stock actual de todos os produtos com quantidade disponível e gráfico de barras','text',NULL,NULL,'2026-04-13 04:50:33.248732',0,3),(28,'assistant','## Relatório de Inventário: Stock Actual\n\n**Resumo executivo:** O inventário actual da exploração apresenta uma distribuição excepcionalmente equilibrada, com os principais produtos e insumos estabilizados em 500 unidades cada, garantindo prontidão operacional imediata.\n\n### Quantidades Disponíveis (Top 10 Itens)\n\nA tabela abaixo destaca os principais produtos em armazém, abrangendo desde a produção final até aos fertilizantes essenciais:\n\n| Produto | Categoria | Stock Actual | Status |\n| :--- | :--- | :---: | :--- |\n| **Laranja Valência Especial** | Fruta | 500 | ✅ Estável |\n| **Laranja Baía do Dombe** | Fruta | 500 | ✅ Estável |\n| **Sumo de Laranja Natural 5L** | Processado | 500 | ✅ Estável |\n| **Polpa de Laranja Congelada** | Processado | 500 | ✅ Estável |\n| **Mudas de Laranjeira Enxertada** | Viveiro | 500 | ✅ Estável |\n| **Ango-Adubo Crescimento Plus** | Fertilizante | 500 | ✅ Estável |\n| **Super-Kwanza Fosfato** | Fertilizante | 500 | ✅ Estável |\n| **Bio-Huambo Orgânico** | Fertilizante | 500 | ✅ Estável |\n| **Ango-Azoto 20-10-10** | Fertilizante | 500 | ✅ Estável |\n| **Sementes de Laranja Certificadas** | Viveiro | 500 | ✅ Estável |\n\n---\n\n### Análise e Recomendações\n\n- **Equilíbrio Operacional:** A uniformidade de 500 unidades em diversos itens (desde frutas prontas a vender até fertilizantes) indica que a logística de reposição está a funcionar de forma sincronizada, ou que houve uma recepção massiva de stock recentemente.\n- **Preparação para a Campanha:** A disponibilidade de fertilizantes específicos como o **Ango-Azoto** e o **Super-Kwanza** em quantidades iguais garante que não haverá falta de nutrientes para as diferentes fases de crescimento das laranjeiras.\n- **Capacidade de Escoamento:** Com 500 unidades de produtos processados (Sumos e Polpas), a empresa está em boa posição para atender encomendas de média dimensão sem roturas imediatas.\n\n---\n> **Quer explorar mais?**\n> 1. Deseja saber o **valor financeiro total** (em Kz) deste stock em armazém?\n> 2. Gostaria de verificar se algum destes produtos está próximo da **data de validade**?\n> 3. Precisa de um relatório de saídas para perceber qual destes itens tem maior rotação?','sql',NULL,NULL,'2026-04-13 04:50:33.254998',0,3),(29,'user','qual é a quantidade total em stock?','text',NULL,NULL,'2026-04-13 04:52:10.262122',0,3),(30,'assistant','A quantidade total de itens atualmente em stock na nossa exploração é de **25.049 unidades**.\n\nEste volume engloba todos os produtos registados no sistema, incluindo a produção de laranjas, derivados processados, fertilizantes e materiais de viveiro.\n\n> **Quer explorar mais?**\n> 1. Deseja ver a distribuição deste stock por **categoria**?\n> 2. Gostaria de saber quais os produtos com **maior volume** em armazém?\n> 3. Precisa de verificar se algum destes itens está abaixo do **stock mínimo**?','sql',NULL,NULL,'2026-04-13 04:52:10.273081',0,3);
/*!40000 ALTER TABLE `cronos_mensagens` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `departamentos`
--

DROP TABLE IF EXISTS `departamentos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `departamentos` (
  `id_dpt` int NOT NULL AUTO_INCREMENT,
  `nome_dpt` varchar(45) NOT NULL,
  `descricao_dpt` longtext NOT NULL,
  `dpt_pai` int DEFAULT NULL,
  `ativo` tinyint NOT NULL DEFAULT '1',
  `responsavel_id` int DEFAULT NULL,
  PRIMARY KEY (`id_dpt`),
  UNIQUE KEY `nome_dpt_UNIQUE` (`nome_dpt`),
  KEY `dpt_pai_idx` (`dpt_pai`),
  KEY `departamentos_responsavel_id_6c48f32a_fk_funcionarios_f_id` (`responsavel_id`),
  CONSTRAINT `departamentos_responsavel_id_6c48f32a_fk_funcionarios_f_id` FOREIGN KEY (`responsavel_id`) REFERENCES `funcionarios` (`f_id`),
  CONSTRAINT `dpt_pai` FOREIGN KEY (`dpt_pai`) REFERENCES `departamentos` (`id_dpt`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `departamentos`
--

LOCK TABLES `departamentos` WRITE;
/*!40000 ALTER TABLE `departamentos` DISABLE KEYS */;
INSERT INTO `departamentos` VALUES (1,'Direção Geral','Departamento responsável pela gestão geral da empresa e definição de estratégias corporativas',NULL,1,32),(2,'Produção Agrícola','Responsável pelo cultivo, manejo, colheita e gestão dos pomares de laranja',1,1,13),(3,'Operações de Campo','Execução das atividades diárias nos pomares: plantio, poda, adubação e colheita',2,1,15),(4,'Gestão de Recursos Hídricos','Gestão e manutenção dos sistemas de irrigação, poços e recursos hídricos',2,1,30),(5,'Controlo de Pragas e Doenças','Monitoramento, prevenção e controle de pragas, doenças e nutrição vegetal',2,1,22),(6,'Pós-colheita e Armazenamento','Processamento, armazenamento refrigerado e conservação das laranjas após colheita',2,1,3),(7,'Controlo de Qualidade','Garantia da qualidade dos frutos, certificações e padrões de exportação',1,1,13),(8,'Laboratório de Análise','Análises de solo, folhas, frutos e controle microbiológico e químico',7,1,12),(9,'Manutenção de Equipamentos','Manutenção preventiva e corretiva de máquinas e equipamentos agrícolas',1,1,6),(10,'Recursos Humanos','Gestão de pessoas, recrutamento, formação e desenvolvimento de colaboradores',1,1,7),(11,'Departamento Financeiro','Gestão financeira, contabilidade, controlo orçamental e tesouraria',1,1,2),(12,'Compras e Suprimentos','Aquisição de insumos, equipamentos, fertilizantes e materiais para produção',11,1,30),(13,'Vendas e Marketing','Comercialização dos produtos, estratégias de mercado e relações com clientes',1,1,2),(14,'Logística e Distribuição','Transporte, armazenamento, distribuição e gestão da cadeia de suprimentos',13,1,8),(15,'Administração e Secretariado','Apoio administrativo, documentação, arquivo e serviços gerais',1,1,9),(16,'Pesquisa e Desenvolvimento','Desenvolvimento de novas técnicas de cultivo, variedades e melhoramento genético',1,1,17),(17,'Segurança e Saúde Ocupacional','Gestão da segurança no trabalho, prevenção de acidentes e saúde ocupacional',1,1,53),(18,'Tecnologia da Informação','Gestão de sistemas informáticos, redes, software e infraestrutura tecnológica',1,1,3),(19,'Relações Institucionais','Relações com instituições públicas, associações e organismos do setor',1,1,4),(20,'Sustentabilidade Ambiental','Gestão ambiental, sustentabilidade, certificações e responsabilidade social',1,1,5);
/*!40000 ALTER TABLE `departamentos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_users_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2026-03-04 13:27:26.706268','2','alcides@dev.com',1,'[{\"added\": {}}]',8,1),(2,'2026-03-04 13:28:20.940789','2','alcides@dev.com',2,'[]',8,1),(3,'2026-03-04 13:34:52.136468','1','gylmiguel07@gmail.com',2,'[{\"changed\": {\"fields\": [\"Username\", \"First name\", \"Last name\"]}}]',8,1),(4,'2026-03-04 14:28:07.407896','2','alcides@dev.com',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Email address\"]}}]',8,1),(5,'2026-03-09 08:52:44.952161','2','alcides@dev.com',2,'[{\"changed\": {\"fields\": [\"password\"]}}]',8,1),(6,'2026-03-09 14:51:15.133713','3','luis.gonzaga',1,'[{\"added\": {}}]',8,1),(7,'2026-03-09 14:52:23.409812','3','luis.gonzaga',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Email address\", \"Staff status\"]}}]',8,1),(8,'2026-03-09 14:53:11.414418','4','erivanio.tiago',1,'[{\"added\": {}}]',8,1),(9,'2026-03-09 14:53:32.331855','4','erivanio.tiago',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\"]}}]',8,1),(10,'2026-03-09 14:54:20.450924','5','waldireny.lua',1,'[{\"added\": {}}]',8,1),(11,'2026-03-09 14:54:57.144985','5','waldireny.lua',2,'[{\"changed\": {\"fields\": [\"First name\", \"Last name\", \"Email address\"]}}]',8,1),(12,'2026-03-09 14:56:19.449853','4','erivanio.tiago',2,'[{\"changed\": {\"fields\": [\"Email address\"]}}]',8,1),(13,'2026-03-09 14:57:18.578935','4','erivaniotiago@gmail.com',2,'[{\"changed\": {\"fields\": [\"Username\"]}}]',8,1),(14,'2026-03-09 14:57:50.039316','3','luisgonzaga@gmail.com',2,'[{\"changed\": {\"fields\": [\"Username\"]}}]',8,1),(15,'2026-03-09 14:58:18.148628','5','waldirenylua@gmail.com',2,'[{\"changed\": {\"fields\": [\"Username\"]}}]',8,1),(16,'2026-03-15 16:50:59.026153','1','Gerente de Produção (Aberta)',1,'[{\"added\": {}}]',14,1),(17,'2026-03-15 16:53:36.308325','1','Gerente de Produção (Aberta)',2,'[{\"changed\": {\"fields\": [\"Num vagas\"]}}]',14,1),(18,'2026-03-15 16:54:01.227435','1','Gerente de Produção (Aberta)',2,'[{\"changed\": {\"fields\": [\"Num vagas\"]}}]',14,1),(19,'2026-03-15 16:56:33.820926','1','Alberto Freguesias -> Gerente de Produção',1,'[{\"added\": {}}]',15,1),(20,'2026-03-15 16:58:01.437957','2','Vaga para técnico de irrigação (Encerrada)',1,'[{\"added\": {}}]',14,1),(21,'2026-03-15 16:59:12.838873','2','Vaga para técnico de irrigação (Aberta)',2,'[{\"changed\": {\"fields\": [\"Estado\"]}}]',14,1),(22,'2026-03-15 17:02:14.903465','2','Vaga para técnico de irrigação (Aberta)',2,'[]',14,1),(23,'2026-03-15 17:05:49.058076','1','Equipas object (1)',1,'[{\"added\": {}}]',2,1),(24,'2026-03-15 17:07:07.191583','1','Equipas object (1)',2,'[]',2,1),(25,'2026-03-15 17:29:09.577601','1','MembrosEquipas object (1)',1,'[{\"added\": {}}]',5,1),(26,'2026-03-15 18:55:48.946022','32','Luís Gonzaga - Gerente de Produção',2,'[{\"changed\": {\"fields\": [\"Avaliacao\"]}}]',4,1),(27,'2026-03-15 19:15:37.708823','82','Yolanda Castelo - Operário Agrícola',2,'[{\"changed\": {\"fields\": [\"Departamento\", \"Avaliacao\"]}}]',4,1),(28,'2026-03-16 12:32:07.158851','2','Joaquim Fernandes - Supervisor Agrícola',2,'[{\"changed\": {\"fields\": [\"Avaliacao\"]}}]',4,1),(29,'2026-03-17 14:08:04.620382','2','alcides@dev.com',2,'[{\"changed\": {\"fields\": [\"password\"]}}]',8,1),(30,'2026-03-17 14:09:12.744961','83','Zeferino Alves - Supervisor Agrícola',2,'[{\"changed\": {\"fields\": [\"Estado\", \"Avaliacao\"]}}]',4,1),(31,'2026-03-17 23:54:42.827287','2','Dimilneia Catihe -> Vaga Para Técnico de Refrigeração',1,'[{\"added\": {}}]',15,1),(32,'2026-03-18 00:09:46.983129','3','José Francisco -> Vaga para Acessor de Recursos Humanos',1,'[{\"added\": {}}]',15,1),(33,'2026-03-18 00:14:22.949713','4','George Washington Jr. -> Vaga para Acessor de Recursos Humanos',1,'[{\"added\": {}}]',15,1),(34,'2026-03-18 10:41:19.376365','3','José Francisco -> Vaga para Acessor de Recursos Humanos',2,'[{\"changed\": {\"fields\": [\"Cv\"]}}]',15,1),(35,'2026-03-18 10:41:38.525668','2','Dimilneia Catihe -> Vaga Para Técnico de Refrigeração',2,'[{\"changed\": {\"fields\": [\"Cv\"]}}]',15,1),(36,'2026-04-01 07:28:34.963470','4','Vaga para Acessor de Recursos Humanos (Encerrada)',2,'[{\"changed\": {\"fields\": [\"Estado\"]}}]',14,1),(37,'2026-04-01 08:07:28.450528','1','Ana Paula dos Santos - Licença Maternidade/Paternidade (2026-03-30)',2,'[{\"changed\": {\"fields\": [\"Tipo ausencia\"]}}]',17,1),(38,'2026-04-11 12:11:35.537571','2','alcides@dev.com',2,'[{\"changed\": {\"fields\": [\"Tipo / Sector\", \"N\\u00edvel\"]}}]',8,1),(39,'2026-04-11 12:11:48.294645','4','erivaniotiago@gmail.com',2,'[{\"changed\": {\"fields\": [\"Tipo / Sector\"]}}]',8,1),(40,'2026-04-11 12:24:34.698348','5','waldirenylua@gmail.com',2,'[{\"changed\": {\"fields\": [\"Tipo / Sector\", \"N\\u00edvel\"]}}]',8,1),(41,'2026-04-11 12:27:35.238147','1','gylmiguel07@gmail.com',2,'[{\"changed\": {\"fields\": [\"Tipo / Sector\", \"N\\u00edvel\"]}}]',8,1),(42,'2026-04-11 12:30:42.563997','1','gylmiguel07@gmail.com',2,'[{\"changed\": {\"fields\": [\"Tipo / Sector\"]}}]',8,1),(43,'2026-04-11 12:30:50.146129','2','alcides@dev.com',2,'[{\"changed\": {\"fields\": [\"Tipo / Sector\"]}}]',8,1),(44,'2026-04-11 12:30:55.788863','4','erivaniotiago@gmail.com',2,'[]',8,1),(45,'2026-04-11 12:31:58.495501','3','luisgonzaga@gmail.com',2,'[{\"changed\": {\"fields\": [\"Tipo / Sector\"]}}]',8,1),(46,'2026-04-11 12:32:12.366201','3','luisgonzaga@gmail.com',2,'[{\"changed\": {\"fields\": [\"N\\u00edvel\"]}}]',8,1),(47,'2026-04-11 12:32:12.397364','3','luisgonzaga@gmail.com',2,'[]',8,1),(48,'2026-04-11 13:01:58.982750','5','waldirenylua@gmail.com',2,'[{\"changed\": {\"fields\": [\"Tipo / Sector\"]}}]',8,1),(49,'2026-04-11 13:30:32.217030','5','waldirenylua@gmail.com',2,'[{\"changed\": {\"fields\": [\"N\\u00edvel\"]}}]',8,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (9,'admin','logentry'),(11,'auth','group'),(10,'auth','permission'),(12,'contenttypes','contenttype'),(18,'cronos','conversacronos'),(19,'cronos','mensagemcronos'),(1,'funcionarios','controlo'),(2,'funcionarios','equipas'),(3,'funcionarios','fdocuments'),(4,'funcionarios','funcionarios'),(5,'funcionarios','membrosequipas'),(17,'funcionarios','planamentferias'),(24,'relatorios','relatorioagendado'),(25,'relatorios','relatoriogerado'),(15,'rh','candidatos'),(6,'rh','cargos'),(7,'rh','departamentos'),(16,'rh','processoseletivo'),(14,'rh','vaga'),(13,'sessions','session'),(21,'stock','categoria'),(22,'stock','fornecedor'),(23,'stock','movimentacao'),(20,'stock','produto'),(8,'users','users');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=59 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'funcionarios','0001_initial','2026-03-02 10:50:54.382128'),(2,'contenttypes','0001_initial','2026-03-02 10:50:54.921757'),(3,'contenttypes','0002_remove_content_type_name','2026-03-02 10:50:55.658461'),(4,'auth','0001_initial','2026-03-02 10:50:57.779384'),(5,'auth','0002_alter_permission_name_max_length','2026-03-02 10:50:58.225924'),(6,'auth','0003_alter_user_email_max_length','2026-03-02 10:50:58.249606'),(7,'auth','0004_alter_user_username_opts','2026-03-02 10:50:58.280844'),(8,'auth','0005_alter_user_last_login_null','2026-03-02 10:50:58.309734'),(9,'auth','0006_require_contenttypes_0002','2026-03-02 10:50:58.334349'),(10,'auth','0007_alter_validators_add_error_messages','2026-03-02 10:50:58.428667'),(11,'auth','0008_alter_user_username_max_length','2026-03-02 10:50:58.465167'),(12,'auth','0009_alter_user_last_name_max_length','2026-03-02 10:50:58.512402'),(13,'auth','0010_alter_group_name_max_length','2026-03-02 10:50:58.598818'),(14,'auth','0011_update_proxy_permissions','2026-03-02 10:50:58.630823'),(15,'auth','0012_alter_user_first_name_max_length','2026-03-02 10:50:58.663412'),(16,'users','0001_initial','2026-03-02 10:51:01.858593'),(17,'admin','0001_initial','2026-03-02 10:51:02.917863'),(18,'admin','0002_logentry_remove_auto_add','2026-03-02 10:51:02.950012'),(19,'admin','0003_logentry_add_action_flag_choices','2026-03-02 10:51:03.007048'),(20,'rh','0001_initial','2026-03-02 10:51:03.028830'),(21,'sessions','0001_initial','2026-03-02 10:51:03.325485'),(22,'funcionarios','0002_alter_funcionarios_options','2026-03-12 16:32:22.619832'),(23,'funcionarios','0003_funcionarios_cargo_funcionarios_data_contratacao_and_more','2026-03-14 19:52:22.792936'),(24,'funcionarios','0004_funcionarios_cargo_funcionarios_data_nasc_and_more','2026-03-14 20:09:41.117546'),(26,'funcionarios','0005_funcionarios_cargo_funcionarios_departamento_and_more','2026-03-15 16:18:05.959181'),(27,'funcionarios','0006_funcionarios_cargo_funcionarios_departamento_and_more','2026-03-15 16:19:59.727407'),(28,'rh','0002_candidatos_processoseletivo_vaga_candidatos_vaga','2026-03-15 16:20:30.444712'),(29,'funcionarios','0007_alter_equipas_options_alter_funcionarios_options_and_more','2026-03-15 17:22:25.769096'),(30,'rh','0003_vaga_num_candidaturas','2026-03-17 22:46:13.398886'),(31,'rh','0004_alter_processoseletivo_options_alter_vaga_options_and_more','2026-03-17 23:43:20.689271'),(32,'rh','0005_candidatos_nota','2026-03-17 23:44:36.832658'),(33,'rh','0006_alter_candidatos_nota','2026-03-18 00:47:34.415165'),(34,'rh','0007_candidatos_fonte_recrutamento_and_more','2026-03-18 10:34:03.662267'),(35,'funcionarios','0008_alter_fdocuments_options_alter_funcionarios_options_and_more','2026-03-19 10:08:48.839275'),(36,'funcionarios','0009_alter_funcionarios_options_funcionarios_cidade_and_more','2026-03-19 10:15:03.730601'),(37,'funcionarios','0010_rename_foto_de_perfil_funcionarios_foto_perfil','2026-03-19 10:16:09.730316'),(38,'rh','0008_alter_departamentos_options_alter_candidatos_cv','2026-03-26 10:53:39.113388'),(39,'funcionarios','0011_alter_funcionarios_estado','2026-03-26 11:01:30.254323'),(40,'rh','0009_remove_departamentos_responsavel_id_and_more','2026-03-26 11:05:02.287550'),(41,'funcionarios','0012_alter_funcionarios_options_funcionarios_iban_and_more','2026-03-26 12:17:27.416970'),(42,'funcionarios','0013_remove_funcionarios_id_controlo_and_more','2026-03-29 21:19:19.172004'),(43,'funcionarios','0014_alter_controlo_options_alter_fdocuments_options','2026-03-29 21:26:40.007255'),(44,'funcionarios','0015_controlo_fun_id_fdocuments_fun_id','2026-03-29 21:42:55.449689'),(45,'funcionarios','0016_ferias_management','2026-03-29 22:48:42.650609'),(46,'funcionarios','0017_planamentferias','2026-03-30 10:12:23.867029'),(47,'cronos','0001_initial','2026-04-02 17:14:31.303370'),(48,'funcionarios','0018_funcionarios_data_demissao_alter_funcionarios_ativo','2026-04-02 17:14:31.405315'),(49,'rh','0010_remove_departamentos_responsavel_id_and_more','2026-04-02 17:14:31.413006'),(50,'users','0002_alter_users_options','2026-04-02 17:14:31.440020'),(51,'users','0003_users_nivel_users_tipo','2026-04-11 12:04:27.992617'),(52,'stock','0001_initial','2026-04-11 15:02:42.472036'),(53,'stock','0002_produto_cod_prod','2026-04-11 15:15:22.502654'),(54,'stock','0003_remove_produto_cod_prod','2026-04-11 15:17:46.203861'),(55,'stock','0004_categoria_prefixo','2026-04-11 15:27:25.870005'),(56,'relatorios','0001_initial','2026-04-13 04:27:13.508784'),(57,'relatorios','0002_remove_relatoriogerado_arquivo_and_more','2026-04-13 04:53:46.365597'),(58,'stock','0005_alter_produto_id_produto','2026-04-13 04:53:46.375715');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('110qv1lydn6twnkj4tn2vk2zwbrh6nmz','.eJxVjEsOwiAUAO_C2hCgSFuX7j0DeR-eVA0kpV0Z725IutDtzGTeKsK-5bi3tMaF1UVZdfplCPRMpQt-QLlXTbVs64K6J_qwTd8qp9f1aP8GGVru28FbnkUMWo_OB0kOkAnFmXkMKEJGGCYPgwEvbpwohDMLs6U0CLD6fAEG1zlw:1wBXyA:NDn2J1o_KQ9gohPVLtacjrH5zI98mU51Bsyb_ky2IGc','2026-04-25 13:01:50.633234'),('1glllqjurhytj95jv5dpcfbmqgn8fuhj','.eJxVjEsOwiAUAO_C2hCgSFuX7j0DeR-eVA0kpV0Z725IutDtzGTeKsK-5bi3tMaF1UVZdfplCPRMpQt-QLlXTbVs64K6J_qwTd8qp9f1aP8GGVru28FbnkUMWo_OB0kOkAnFmXkMKEJGGCYPgwEvbpwohDMLs6U0CLD6fAEG1zlw:1w2AYX:6L3XrwjPuZzNGDYF4_8PIQlLEwCWb7MJ3RGdxLKge8E','2026-03-30 16:12:37.219828'),('3e5kbshpmj06ceeayv2eh6bmcm2kpuxd','.eJxVjEsOAiEQBe_C2hDA5tMu3XsG0kArowaSYWZlvLtOMgvdvqp6LxFpXWpcB89xKuIkrDj8bonyg9sGyp3arcvc2zJPSW6K3OmQl174ed7dv4NKo37ro_fKu2LRIBt2VsHVZKUDEwAG0iqRVQjsM3mDCGhc0pnAhaJNUk68P7ZLNrk:1w3AqC:k0jOyoAJ9JqmWYZuYuSjZO4WQBmnwJgP9-DhlgdNZrY','2026-04-02 10:43:00.222762'),('50flguga0zx77eqxcl7v6ckqgup0b9yp','.eJxVjMsOwiAQAP-FsyE8yoIevfsNZHcBqRqalPZk_HdD0oNeZybzFhH3rca95zXOSVyEEadfRsjP3IZID2z3RfLStnUmORJ52C5vS8qv69H-DSr2OraQi9HgFBqmQDpZwMKuWLRglZ8Cl3A2SgEEawn8pHRhJKIcWHlXxOcL2Tc3ww:1wBzLa:iUQw5inLzvSzqgVY_R2af1hXrDIs07k4FES7dQ51W0A','2026-04-26 18:15:50.077265'),('58e060cz8eg285n3zhrfeqfpdfblwspi','.eJxVjEsOAiEQBe_C2hDA5tMu3XsG0kArowaSYWZlvLtOMgvdvqp6LxFpXWpcB89xKuIkrDj8bonyg9sGyp3arcvc2zJPSW6K3OmQl174ed7dv4NKo37ro_fKu2LRIBt2VsHVZKUDEwAG0iqRVQjsM3mDCGhc0pnAhaJNUk68P7ZLNrk:1w3AhO:NmInxYUpBFTD7NF_hTnzG1VIIGBGVaT07G82bOjO_Xs','2026-04-02 10:33:54.765340'),('6k8hu2hk5dr51tkkssy1aay02hprk60r','.eJxVjEsOwiAUAO_C2hCgSFuX7j0DeR-eVA0kpV0Z725IutDtzGTeKsK-5bi3tMaF1UVZdfplCPRMpQt-QLlXTbVs64K6J_qwTd8qp9f1aP8GGVru28FbnkUMWo_OB0kOkAnFmXkMKEJGGCYPgwEvbpwohDMLs6U0CLD6fAEG1zlw:1wBXyA:NDn2J1o_KQ9gohPVLtacjrH5zI98mU51Bsyb_ky2IGc','2026-04-25 13:01:50.722238'),('6l75tnyhgleeh5df0qzhxomi81d4c7lu','.eJxVjEsOwiAUAO_C2hCgSFuX7j0DeR-eVA0kpV0Z725IutDtzGTeKsK-5bi3tMaF1UVZdfplCPRMpQt-QLlXTbVs64K6J_qwTd8qp9f1aP8GGVru28FbnkUMWo_OB0kOkAnFmXkMKEJGGCYPgwEvbpwohDMLs6U0CLD6fAEG1zlw:1wAV4R:Sqer1gNuK-rLCIdxa_dYGwAH0mlgpj6pWLmfHQ8oQcg','2026-04-22 15:43:59.104982'),('7ee6ibpj5sezp06yi5rlx7l72jjfhu91','.eJxVjEsOwiAUAO_C2hCgSFuX7j0DeR-eVA0kpV0Z725IutDtzGTeKsK-5bi3tMaF1UVZdfplCPRMpQt-QLlXTbVs64K6J_qwTd8qp9f1aP8GGVru28FbnkUMWo_OB0kOkAnFmXkMKEJGGCYPgwEvbpwohDMLs6U0CLD6fAEG1zlw:1wAV4Q:0coIfybTtNrxoulJHK4GZZs0g3OhKBbD1OxYTVaCiWw','2026-04-22 15:43:58.212040'),('drt3dk0ro6kq8tm74wii4jolsboymml5','.eJxVkkFz0zAQhf_K4mMmeJy4cdJeGOiUGwTaI2Eya3llb5AlI8mBodP_zsoxpb14ZO3bb9_b0WN2xDF2xzGQP3KT3WTrbPnyrkb1g2wqNCe0rcuVs9FznSdJPldD_sk1ZD7M2leADkOXsBXp9araFLhW9a5eNWWFWm10iWVVFturndK763VRVNWuLOtqe1WstMK6rmmniu1GC1R5Z104dhyi86xcdvPtMfPOkODTqCQRc2SjXHwdqQftGBxEGkF5xsb5d9nT8rkHQxAUivxl494cxqKg1Ru4GyG4UQCLxe39_vP-YbFYAgKL0nA7qdAqRkAfWbOcDFiMfEZoUtPd_Rd47yP1HBaL_GAP9uPI0FAge3bmzCIayCDQz5EH6SEg25LtULwCQSOGg3yFNFPgwen4Cz0JDwb0CJL6zB6U690c9BJKotA_o9PZIrQU4mS6dED9IJQ0yOSwh14aB--GVNZl4OhgUl6DRsWGI3rBo6IQ5kohdO18j9PfduYuwRMa_iNytJc1Gg4UksHB0G8MKeUlGAGexgb9W3GHEF0vTQ0pDpOJjTSJX48Xy9ctK5wwUGOQONNmEkYG8rSlOCI436KV8a9MTZu_TRsaXPL_f2zCPYMEMW8FOncieSnfn_4CJxcRvQ:1wBZSd:EJfVbxJ3NROryXViIfcxsgA03YHAqEvwOKrmBCKbZu8','2026-04-25 14:37:23.850769'),('frq1gmiw70q65ko4gk3qaxl0x1rsj6i9','.eJxVjEsOwiAUAO_C2hCgSFuX7j0DeR-eVA0kpV0Z725IutDtzGTeKsK-5bi3tMaF1UVZdfplCPRMpQt-QLlXTbVs64K6J_qwTd8qp9f1aP8GGVru28FbnkUMWo_OB0kOkAnFmXkMKEJGGCYPgwEvbpwohDMLs6U0CLD6fAEG1zlw:1w0eEI:4m2p7XqmAYNZtBVk3X0QaEDGfNeBIgHfCjfpedvgfAM','2026-03-26 11:29:26.079731'),('h1ae54kjuh4kkb5zkvh8tmft8wha6ik3','.eJxVjEsOwiAUAO_C2hCgSFuX7j0DeR-eVA0kpV0Z725IutDtzGTeKsK-5bi3tMaF1UVZdfplCPRMpQt-QLlXTbVs64K6J_qwTd8qp9f1aP8GGVru28FbnkUMWo_OB0kOkAnFmXkMKEJGGCYPgwEvbpwohDMLs6U0CLD6fAEG1zlw:1w2AYX:6L3XrwjPuZzNGDYF4_8PIQlLEwCWb7MJ3RGdxLKge8E','2026-03-30 16:12:37.153033'),('hg0299wt4ts4v0j5iijfhsvqo1krco41','.eJxVjEsOwiAUAO_C2hCgSFuX7j0DeR-eVA0kpV0Z725IutDtzGTeKsK-5bi3tMaF1UVZdfplCPRMpQt-QLlXTbVs64K6J_qwTd8qp9f1aP8GGVru28FbnkUMWo_OB0kOkAnFmXkMKEJGGCYPgwEvbpwohDMLs6U0CLD6fAEG1zlw:1w2AYZ:2N-aypOx3luNzYHHjd_i9znKnMpg9qP5aQTJre5bKgg','2026-03-30 16:12:39.419979'),('iwspn7g5s90votlr9edaoy6wuo1h3c1w','e30:1vxmI9:LEP1poma_7hHLUNxRlXLxTkvhaHpdVOBPPaazmwnXZY','2026-03-18 13:29:33.530480'),('iy945i6n9rqhajbh1ns4hw6x9j2ooxu8','.eJxVjDsOwjAQBe_iGlnr-LempOcM1q69JgGUSPlUiLtDpBTQvpl5L5VpW_u8LTLnoaqzsur0uzGVh4w7qHcab5Mu07jOA-td0Qdd9HWq8rwc7t9BT0v_rT1K840gFmvYWV-wYRWE1JXUwIMFJzG5YBJi42i6gMEJVWaIBhyp9wfYyDdQ:1wCBow:AuTd0p8OfDRF9NKaonKwaeY5cfHbRDj2K4fYU4yiZaw','2026-04-13 11:34:58.434855'),('j25kndn90a63phfil9p3iz24ato28ebh','.eJxVjEsOwiAUAO_C2hCgSFuX7j0DeR-eVA0kpV0Z725IutDtzGTeKsK-5bi3tMaF1UVZdfplCPRMpQt-QLlXTbVs64K6J_qwTd8qp9f1aP8GGVru28FbnkUMWo_OB0kOkAnFmXkMKEJGGCYPgwEvbpwohDMLs6U0CLD6fAEG1zlw:1w2V5Y:tgR-p9Q23Vow22q0AOyw1bd4gp1Sspi8XpERg3_knWI','2026-03-31 14:08:04.773486'),('jbemwcwmzamyk2wj1p5txt1mjgd31ziz','.eJxVjEsOwiAUAO_C2hCgSFuX7j0DeR-eVA0kpV0Z725IutDtzGTeKsK-5bi3tMaF1UVZdfplCPRMpQt-QLlXTbVs64K6J_qwTd8qp9f1aP8GGVru28FbnkUMWo_OB0kOkAnFmXkMKEJGGCYPgwEvbpwohDMLs6U0CLD6fAEG1zlw:1w2AYX:6L3XrwjPuZzNGDYF4_8PIQlLEwCWb7MJ3RGdxLKge8E','2026-03-30 16:12:37.430365'),('kvey4mrquaypavqvbb9tm75kuekh56bd','.eJxVjDsOwjAQBe_iGlnr-LempOcM1q69JgGUSPlUiLtDpBTQvpl5L5VpW_u8LTLnoaqzsur0uzGVh4w7qHcab5Mu07jOA-td0Qdd9HWq8rwc7t9BT0v_rT1K840gFmvYWV-wYRWE1JXUwIMFJzG5YBJi42i6gMEJVWaIBhyp9wfYyDdQ:1wBZsi:egGKhXLmfdT9wSDKZdXL4-FTssv926OBSU6Yx_jkoLM','2026-04-25 15:04:20.590927'),('l5lv4vciibpjssvvs3hj439ttqn9zs4v','.eJxVjEEOwiAQRe_C2pDqwFBcuvcMZIYBqRpISrsy3l2bdKHb_977LxVoXUpYe5rDJOqsjDr8bkzxkeoG5E711nRsdZkn1puid9r1tUl6Xnb376BQL98aQFCceIjZ22goMiCNkTkTCZrEFnwa0BHzCNmbzCiG5ehOCBYGp94fGDY4yQ:1wBXGO:WITuapYAVeloDGnGXxX_rusXusB3c8Z1nqHSTA-htBw','2026-04-25 12:16:36.395203'),('limr8vng867w0kr5mkfzaggox841henw','.eJxVjEsOAiEQBe_C2hDA5tMu3XsG0kArowaSYWZlvLtOMgvdvqp6LxFpXWpcB89xKuIkrDj8bonyg9sGyp3arcvc2zJPSW6K3OmQl174ed7dv4NKo37ro_fKu2LRIBt2VsHVZKUDEwAG0iqRVQjsM3mDCGhc0pnAhaJNUk68P7ZLNrk:1w5iJa:Vp51RVZrA_JdDrhY195OlV27t01pnc-AQpNh6JBS5AA','2026-04-09 10:51:50.234168'),('nxr3945x3we4c8kzk0hw25q5uo02bf6f','.eJxVjMsOwiAQAP-FsyE8yoIevfsNZHcBqRqalPZk_HdD0oNeZybzFhH3rca95zXOSVyEEadfRsjP3IZID2z3RfLStnUmORJ52C5vS8qv69H-DSr2OraQi9HgFBqmQDpZwMKuWLRglZ8Cl3A2SgEEawn8pHRhJKIcWHlXxOcL2Tc3ww:1wC7k4:z2zzM3YLZchSOSG0XhGKDZqR6zSfb9u0niwco-iUbas','2026-04-27 03:13:40.326821'),('q4j35qqjqun20hpjsj1hvouk09tpgt8g','.eJxVjEsOwiAUAO_C2hCgSFuX7j0DeR-eVA0kpV0Z725IutDtzGTeKsK-5bi3tMaF1UVZdfplCPRMpQt-QLlXTbVs64K6J_qwTd8qp9f1aP8GGVru28FbnkUMWo_OB0kOkAnFmXkMKEJGGCYPgwEvbpwohDMLs6U0CLD6fAEG1zlw:1w0hH7:NSlYOXlCXisushFNFsp_65n-6lrJUQZXIurLJ22du2o','2026-03-26 14:44:33.473822'),('swrefmqi0holgafolbgogoeefwl5lj4s','.eJx1VWFPGzkQ_Suj8KEQhSghFAofinJHr0JqdUCrfjkqOmuPE_e89tZeR1yr_veb8W5CAu2XJLvrnffmvTeTH4N7zO3yPieK91YPzgfTwWj7XoXqX_LyQH9FvwhjFXwbbTWWI-P-aRq_D5rcH_3ZnQJLTEspOzue6jNjJtX0uDo6PjF0hJVWlTmanJ2eVMaoidH46hhnEzw2R6ev1MnJS220niqaGZSiKgYf0v3SpjZEq8Lg_J8fgxgccXmBkiNMjnzLN24y-jYkMNkrG_xdnkxoGi3faanmTx-gDS06IFChDkCpLWdmATQDcIe5XGvNh5sQIdEDn5JzqAMou7LuYvBztGGAKfF7DLpDY28PbslhqW1mjA-a4LIHsAXhdINL8NdTtnf-zg-Ht5SycHwglVu7CufDIVwS1KFmlDACvy5Rvs-Yb0od-xU5aGJQlBJGQBBmuKCaO9G_YfFL0TStLLeNkGsEg26J0Ol1prxVKNzZcmbDF7v1WGgU-J7cBCpMJOc165jG0uAeq_Sm01Uj_Bl8yq7FO3_lDTn7XZqkEQQVYqTMDIBiLHI1FGvbt8pQ-1_mSqD4kbekvxwAssv8trSuSFPsOXAIsGJb-GSAN7fXMI-cCpvGQoNEsMpRvdNiAFs3XOKwLuTpoY1oI4g00gdEQpsghSoSrKOlJVsOqxD5SKQ0goqVL3Fj6JQF_7kJ5iX9NnEbuf6Gb1mA4tNwrdiIhrG6rvcllXV_trfBcOkoRbPQOji_89cYUW41wT9qJPy4H2eVbXctZStAsi4KrcdmKskydlFqQiMF0aOznDoGGALAcPgpuMzqfRRtJMHzrTQ-oGpLitogahZBFzLoPKnYuyWPnyVzvK5-aVcUk2U3ikFvO-s8xdBhsaks6m42WaT4xCOoMansLG8a1t5wKrz83sBcUzTWwYeg7LqLRAuJ6JPci4Pb1nWiSJSLyNJNHRYRjUVJPdXiGhaDDw8P1z7P-1ZZSU4C7xIlM69xNy78iuhL0Zpn88dazIvxQnb9fiiRKPKrtmRDS6OcRVFBpmJtcMhMlb5l2xT9P151fax6rChJ3hrDEl5-ndcUT24p9gKdsprSC1kFvKZlkUR4_9-Hm3fjjvi1GNcHCdlfLGMZO-fKRJaB75cbs_CPy42vrDcRWeqY2ywSj8qSWtF3yXRwgjdiO1h1srCgiMUYkTPkNpaobQ9R4kknbbHFsni2HXnNZG8yu0cPjQtSqOapvxgOpY9LHrqvWITlLSVrh7ZkSlsTiGvgugPV2fHFflkMn8TdJLJf-RXX2CT9YGvW-ilAdyHAbwPHLNriT-JJicyhLKN1BLi4wropa7xfV8Ky-yPkDdSEjaC2zBtTXv5y3DrzTRE68YQ_hjPxn-Hnn_8DdP3hlw:1w8GWe:YIfioHK8pjOGUl2hp0fKf1a0ZGn1TMMMSXC1v6gLAIU','2026-04-16 11:47:52.810180'),('t7txqapfch8rciq0g1dsw95w4woml33k','.eJylWF1z2zYW_SsY56G2RuboW7IfNuPYSZtpvXbiTl7qncwVCUloSIIGSNWTOv99zwVIiqTsru2dSZuQAi7ux7nnHvDvg69U5JuvhZXmq4oOTg_GB_3muyWF32TKP0R_UrrWQajT3KhlwEuC8lcbXOpIxu_KtS0DG7Ib7J4u5Gq6osE8HA-Xk_E0XKwWkVwMTkbhyWowHYwHEzk_mcyGJ4vFajkfjmaL2URStFwO5sPBhGA0NDrV9utG2VwbFeqD0z_-PjA6ljDPR_ESOCfTHC9-loZEkQgjY8pvi8FgNTZKi1AnWSxzLSIpQspUTrHYFAml7idBKS-Vw1hZKSzFZBQWZNpgfUYmpwTWtZBibfzCFfvxo1_7QdbCPYILTWfevBGf237g-PPy-F_88VKcNQ-_KQ-_TW_TXu-ztEWCNfcyLHK11ae9njgT0uamyAsEWrsaERZlsTbkbM3d_8daUGakhTOcE0KoaYiH7iI4pdItrCofJrLdipufhC2QjlyKWK_dvgjLQ3afM72zt5pKC2v4MS9CpVNStu9SrIVF_jmh4trnwx6HOt5IJEMQrFSeGjwlpLB0RbkiDi1BehvB5hr5CzhDb5DhCyQewCxUO6ibZhUvmlU8_F1nYjg4uk3PRE5LuC9oSeqeEwHDGxKIOCwsB77Ca-v8z6S1Gub2k8O_eodVklGIE1YqJWRaGX3KXj60z38Q5zqmJWoVacSM50sXX-3x4a_fj_itC-UkUns_scnT4-Nj4f863f-bV_R6-4kG2kxC32XqfQGcHsRE8NpxMJkOgsFg0B8M3OvFbBRM3WNl7vN-pT-2Ku32jZ057O2Yqx9r76S9K5Rlpy649Fsdb1XXrVEwmLfsTIfzjls3co1e8E00Z2s3zssVAWpXYYGSsHex2z2qjA5aRoeNF5XZ31yJ2r3bbFXvjbM3DBaTlr3xbNGxdg4CMmTZuyIzPkzbiHMYTOYdE904z6JEpQz2TvvCpAwNoAuERLpRg2G3pJPFOBiPx_3xeOcW6EDHLrhPBcUqQtbaJtqZmsxmwWw268_mlYlLSgvw3R6lvEdxM2oEWlkcj9oWJ93MX2XSdIHmiDPJdCtlo07KWtC4TdEKFUm0OFaCldG0GFmdU9wmWH5vMxmi3dT3Tqp_9y0Zpiok5uKr9nyAky-BY6atLVRNd8mu32uqO2whE83fB5HeFUzYEXzAXk-b1Wk4466gyICWKPZuuTexwsQCOhiAIDKZIjxlBXxnG5gLK20SV3wRy_XTAyXwCfqgQf2uTD4YnwsZyy3OaA8TmTyTiCKZ6JTR7eLDioRD4wCRHFSiitVsu-OLfITOezwgdZT-ifVZeaqL0J_bF2v-NUf6NDK5pZhHkoZlHRUlc8dlkFc88Iq0tMug2SpbHsoBX3SngMamL4wqzvIlmW8S56yxkmFxoYxs-81ShWFQz-jE-wO0LwkwTQoFj9xksgDCqAmDYAfhYyzdSuMKbATD2-YwgYc1l9vmu57cIhYPCZk6mDhE6IJ3pTIEMBR7gVhZLZhGvCJF9nXsJ3_OyHOigdUEZEkJJHDQIzyAkeoyVGb1Pfz0o5oYhDum8Bh6Fu_6RhG63X3lHOZSNMfr4RRNAwWB_1Kfi5PExfdYv0m4Eqsl9gIqtlgjr4wUXr5TXXBIOpfdkZFaScNJtcJ7GW2l8pJJpgxdxk9Q89G_EOKnQpqqvYzz-W2vxz8NAzcKAV5UFLCNWVRWsiRyJ6-KlHvO5wPpsQzfLgvt9dtbtj4KxM_aujnhdDBGErEDvMWi3WS6gToigFC1W-zIKzjLeWocDK1TsO9sexyIawPStOThAzA46crneClFsE8lUlhZ7cUhedMatCF-kltEgp7-6W1TZO-J_Uvt-ALSMtfhN-9P7DCnHbBt1ddepAHygKtvZ2UzXZcr7ih7NrEkg3n9So3_MeUA6thOxY1z8Mw5-LS0v3LU2dhYh_QseR89roTlfSgzz9Nl8zdBXlYWLIt6ZG4oVDnjDmcnHYvQUvE8jHyhMGZFSY1MNVGbWGGBE105oHeDAhJZouFyquX7p7oolqV8oypwpZTq4iOSbY94y75kh2shPRkC7nY8Z8q-72MbvFzL1DWNjaSbKljcTpkbA4JKuhDEeJUmdxlwnb6boaXCvy4HCMQ95XKtucceWmV3j5QXdk-_d-T7ToD6OfalbDrPl5U2cYrnAxiJz-FyPIAWIYimWFECiIHdsfXOA4ipRIsLnSzly-zclD1d2fs3MSPGYvqbs4Ms8BRhEfAMY9c6zqhpDWp0jdpG9ApjlwXP3doYLl_IVXqPqlX2vqgtX8meY-wsXevjs6hYanGODgtLLXMdF17KfmiA4XlpQwsc__oXpdAxH7TFzVa_ytA7pY9_KSiBY1fGX8RHEKOvM-aj_K4R2WhwPOQ_r4tOJn7-NUvJNpzmJPuS7P8_qp1pzcN7ydzZ0adnTFg7mYs_LRKTPMkxdS16XTHdiENPECvuDes5jVhLgqEjns4VO7SY4ahS5l7Etr6WOKwbCdnfZegqCdhRzkVyX0rYXagT8BpOZ_YFz0Kuse2NLraVTgO_tw3yBxO1def50chr4J6rUynEMK55Frc3lhcCvmpRuiGfNz8sFQ-AKnVdNgQn-Th5fJZiWLcg5mSw7vQCv2zOZaR-zZKiHCbSRZpWzm0I9SkTteLrDXuCy6dRHn7eedtUZCsIaYfLsNHGTBRxzRKVMD0nvppVAb63ofZ6inOA23sbLVhRz5is5ilg5sbPS-G4zUJ57i4yuyoj5qVmQd0Fgo8g9wDDgPFwd8c11GrEcdTK3LJu0kzDtp6u9sV602KqGlcffyfafcLyn9uQhEMcxJ-feORWuOrM18dkZutuQvG6SLyF5pSuM5MZr6PuVeIudr1eRL7O2_rjxFN6syvCbDnrokp1Aneh5DDvvEx0TvheR2uUt3Ckst0T_yxBnalKJjQVpssa58cl6u3_FpJn-7v5juXcIxYQpXgrLfKNLNX83fBRZVi65L5IjKbBYHJSg7fXc-h4z1Xc6rhI-Dq4jvWSHtHNrMjhK79OgTX8WyYgITBSXDit96h-4s8IfhDYPh6M2joLjU7pdykE6c-xkPzVaeunhXP0RTemJzRwE7P8QbjXCyuZVgKqg1rfD3eOjLr3iF7PQ8Unz3PYXhe0Afp0E_gCNyZAqWu5Fb2_vvOjFC0BXw9-_OfHfwEmX5ps:1wC9it:k_EniOQz_v-eMgtTf7AOlujDauPBt19M_Y9d99my0ks','2026-04-13 09:20:35.132211'),('xvkxgbxfngjgcmllmk9fraliovpg5yib','.eJxVjEsOwiAUAO_C2hCgSFuX7j0DeR-eVA0kpV0Z725IutDtzGTeKsK-5bi3tMaF1UVZdfplCPRMpQt-QLlXTbVs64K6J_qwTd8qp9f1aP8GGVru28FbnkUMWo_OB0kOkAnFmXkMKEJGGCYPgwEvbpwohDMLs6U0CLD6fAEG1zlw:1w25Wt:JanQzVHIa3v0LAz31QED74gCE0-U1T1Rm6HF1wmKUBI','2026-03-30 10:50:35.698796'),('yoz5zix3dl8bw2cdattc6ssvhozvil9g','.eJxVjDsOwjAQBe_iGlnr-LempOcM1q69JgGUSPlUiLtDpBTQvpl5L5VpW_u8LTLnoaqzsur0uzGVh4w7qHcab5Mu07jOA-td0Qdd9HWq8rwc7t9BT0v_rT1K840gFmvYWV-wYRWE1JXUwIMFJzG5YBJi42i6gMEJVWaIBhyp9wfYyDdQ:1wBZsj:Vcy8E9DJkGn8jXsJW8jwkBrg3608wIq0omLwKRvW4x4','2026-04-25 15:04:21.983338');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `equipas`
--

DROP TABLE IF EXISTS `equipas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `equipas` (
  `id_equipas` int NOT NULL AUTO_INCREMENT,
  `nome_equipa` varchar(45) NOT NULL,
  `responsavel_equipa` int DEFAULT NULL,
  `departamento_id` int DEFAULT NULL,
  `data_inicio` date NOT NULL,
  `data_fim` date DEFAULT NULL,
  `ativo` tinyint NOT NULL DEFAULT '1',
  `tipo_equipa` enum('permanente','projecto','temporaria') NOT NULL DEFAULT 'projecto',
  PRIMARY KEY (`id_equipas`),
  UNIQUE KEY `nome_equipa_UNIQUE` (`nome_equipa`),
  KEY `equipas_ibfk_1` (`departamento_id`),
  KEY `equipas_ibfk_2` (`responsavel_equipa`),
  CONSTRAINT `equipas_ibfk_1` FOREIGN KEY (`departamento_id`) REFERENCES `departamentos` (`id_dpt`),
  CONSTRAINT `equipas_ibfk_2` FOREIGN KEY (`responsavel_equipa`) REFERENCES `funcionarios` (`f_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `equipas`
--

LOCK TABLES `equipas` WRITE;
/*!40000 ALTER TABLE `equipas` DISABLE KEYS */;
INSERT INTO `equipas` VALUES (1,'Team Power Ranger da irrigação',11,3,'2026-03-15','2026-06-01',1,'temporaria');
/*!40000 ALTER TABLE `equipas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `f_documents`
--

DROP TABLE IF EXISTS `f_documents`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `f_documents` (
  `id_docs` int NOT NULL AUTO_INCREMENT,
  `bi` varchar(255) NOT NULL,
  `passaporte` varchar(255) DEFAULT NULL,
  `atestado` varchar(255) DEFAULT NULL,
  `certificado` varchar(255) DEFAULT NULL,
  `contracto` varchar(255) NOT NULL,
  `f_id` int DEFAULT NULL,
  PRIMARY KEY (`id_docs`),
  UNIQUE KEY `bi_UNIQUE` (`bi`),
  UNIQUE KEY `contracto_UNIQUE` (`contracto`),
  UNIQUE KEY `passaporte_UNIQUE` (`passaporte`),
  UNIQUE KEY `certificado_UNIQUE` (`certificado`),
  UNIQUE KEY `atestado_UNIQUE` (`atestado`),
  KEY `f_documents_f_id_57927344_fk_funcionarios_f_id` (`f_id`),
  CONSTRAINT `f_documents_f_id_57927344_fk_funcionarios_f_id` FOREIGN KEY (`f_id`) REFERENCES `funcionarios` (`f_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `f_documents`
--

LOCK TABLES `f_documents` WRITE;
/*!40000 ALTER TABLE `f_documents` DISABLE KEYS */;
/*!40000 ALTER TABLE `f_documents` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `funcionarios`
--

DROP TABLE IF EXISTS `funcionarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `funcionarios` (
  `f_id` int NOT NULL AUTO_INCREMENT,
  `f_nome` varchar(45) NOT NULL,
  `cargo` int DEFAULT NULL,
  `estado` varchar(45) NOT NULL,
  `avaliacao` longtext,
  `contacto` varchar(25) NOT NULL,
  `contacto_alt` varchar(45) DEFAULT NULL,
  `naturalidade` varchar(45) DEFAULT NULL,
  `nacionalidade` varchar(45) NOT NULL,
  `sexo` varchar(45) NOT NULL,
  `estado_civil` varchar(45) NOT NULL,
  `banco_nome` varchar(45) NOT NULL,
  `conta_bancaria` varchar(45) NOT NULL,
  `departamento_id` int DEFAULT NULL,
  `ativo` varchar(15) NOT NULL,
  `data_contratacao` date DEFAULT NULL,
  `data_nasc` date DEFAULT NULL,
  `cidade` varchar(45) DEFAULT NULL,
  `endereco` longtext,
  `foto_perfil` varchar(100) DEFAULT NULL,
  `num_bi` varchar(45) DEFAULT NULL,
  `provincia` varchar(45) NOT NULL,
  `iban` varchar(45) DEFAULT NULL,
  `supervisor_id` int DEFAULT NULL,
  `titular` varchar(45) DEFAULT NULL,
  `data_demissao` date DEFAULT NULL,
  PRIMARY KEY (`f_id`),
  UNIQUE KEY `contacto_UNIQUE` (`contacto`),
  UNIQUE KEY `conta_bancaria_UNIQUE` (`conta_bancaria`),
  UNIQUE KEY `num_bi` (`num_bi`),
  KEY `cargo_idx` (`cargo`),
  KEY `funcionarios_departamento_id_c0c2a5d2` (`departamento_id`),
  KEY `funcionarios_supervisor_id_0df28f29_fk_funcionarios_f_id` (`supervisor_id`),
  CONSTRAINT `cargo` FOREIGN KEY (`cargo`) REFERENCES `cargos` (`id_cargo`),
  CONSTRAINT `funcionarios_departamento_id_c0c2a5d2_fk_departamentos_id_dpt` FOREIGN KEY (`departamento_id`) REFERENCES `departamentos` (`id_dpt`),
  CONSTRAINT `funcionarios_supervisor_id_0df28f29_fk_funcionarios_f_id` FOREIGN KEY (`supervisor_id`) REFERENCES `funcionarios` (`f_id`)
) ENGINE=InnoDB AUTO_INCREMENT=105 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `funcionarios`
--

LOCK TABLES `funcionarios` WRITE;
/*!40000 ALTER TABLE `funcionarios` DISABLE KEYS */;
INSERT INTO `funcionarios` VALUES (1,'Manuel da Silva',10,'efetivo','100','923456789','manuel.silva1@artemis.com','Luanda','angolana','M','casado','BAI','00345678901234567890',1,'demitido','2024-05-06','2005-11-27',NULL,NULL,'',NULL,'luanda',NULL,NULL,NULL,'2026-04-03'),(2,'Joaquim Fernandes',2,'efetivo','76','923456790','joaquim.fernandes2@artemis.com','Huambo','angolana','M','solteiro','BPC','00345678901234567891',2,'afastado','2024-01-22','1996-05-12',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(3,'Ana Paula dos Santos',3,'efetivo','61','923456791','ana.santos3@artemis.com','Lisboa','portuguesa','F','casada','BFA','00345678901234567892',3,'ferias','2025-01-18','2000-02-03',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(4,'Erivânio Tiago',4,'efetivo','60','923456792','erivanio.tiago4@artemis.com','Luanda','angolana','M','solteiro','BAI','00345678901234567893',4,'afastado','2024-07-16','2005-05-16',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(5,'Maria Fernanda',5,'efetivo','97','923456793','maria.fernanda5@artemis.com','Porto','portuguesa','F','casada','BNI','00345678901234567894',5,'afastado','2024-07-05','1992-08-03',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(6,'Pedro Miguel',6,'efetivo','84','923456794','pedro.miguel6@artemis.com','Uíge','angolana','M','solteiro','BCS','00345678901234567895',6,'afastado','2024-12-08','1996-10-28',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(7,'Luísa Costa',7,'efetivo','30','923456795','luisa.costa7@artemis.com','Coimbra','portuguesa','F','solteira','ATLÂNTICO','00345678901234567896',7,'afastado','2024-12-14','2000-05-14',NULL,NULL,'',NULL,'luanda',NULL,NULL,NULL,NULL),(8,'António Domingos',8,'efetivo','66','923456796','antonio.domingos8@artemis.com','Malanje','angolana','M','casado','BAI','00345678901234567897',8,'ativo','2025-12-15','2005-05-10',NULL,NULL,'',NULL,'luanda',NULL,NULL,NULL,NULL),(9,'Sofia Matias',1,'efetivo','69','923456797','sofia.pereira9@artemis.com','Luanda','angolana','F','solteira','BPC','00345678901234567898',9,'afastado','2024-04-26','2005-09-06','Luanda','Rua da Dira','','012233445LA89','Luanda','',NULL,'Sofia Pereira Matias',NULL),(10,'José Eduardo',2,'efetivo','87','923456798','jose.eduardo10@artemis.com','Huíla','angolana','M','casado','BFA','00345678901234567899',10,'afastado','2024-02-16','1992-05-06',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(11,'Catarina Martins',3,'efetivo','88','923456799','catarina.martins11@artemis.com','Aveiro','portuguesa','F','solteira','SOL','00345678901234567900',11,'ativo','2025-11-16','1994-09-04',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(12,'Francisco Lopes',4,'efetivo','77','923456800','francisco.lopes12@artemis.com','Cabinda','angolana','M','solteiro','BNI','00345678901234567901',12,'afastado','2024-03-18','2004-05-05',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(13,'Isabel Monteiro',5,'efetivo','63','923456801','isabel.monteiro13@artemis.com','Lisboa','portuguesa','F','casada','BCS','00345678901234567902',13,'afastado','2026-01-10','2003-09-13',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(14,'João Baptista',6,'efetivo','64','923456802','joao.baptista14@artemis.com','Bié','angolana','M','solteiro','ATLÂNTICO','00345678901234567903',14,'afastado','2024-09-14','1999-06-19',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(15,'Teresa Oliveira',7,'efetivo','70','923456803','teresa.oliveira15@artemis.com','Braga','portuguesa','F','casada','BAI','00345678901234567904',15,'ativo','2025-11-04','1994-03-22',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(16,'Miguel Ângelo',8,'efetivo','60','923456804','miguel.angelo16@artemis.com','Luanda','angolana','M','solteiro','BPC','00345678901234567905',16,'afastado','2024-07-03','1994-09-19',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(17,'Inês Rodrigues',1,'efetivo','72','923456805','ines.rodrigues17@artemis.com','Porto','portuguesa','F','solteira','BFA','00345678901234567906',17,'ativo','2025-05-22','1998-12-02',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(18,'Rui Alexandre',2,'efetivo','79','923456806','rui.alexandre18@artemis.com','Huambo','angolana','M','casado','SOL','00345678901234567907',18,'afastado','2025-01-13','2004-06-15',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(19,'Marta Sousa',3,'efetivo','76','923456807','marta.sousa19@artemis.com','Setúbal','portuguesa','F','solteira','BNI','00345678901234567908',19,'ativo','2025-01-03','2005-07-06',NULL,NULL,'',NULL,'luanda',NULL,NULL,NULL,NULL),(20,'Paulo Jorge',4,'efetivo','86','923456808','paulo.jorge20@artemis.com','Cuanza Norte','angolana','M','casado','BCS','00345678901234567909',20,'afastado','2025-12-07','1994-03-14',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(21,'Beatriz Nunes',5,'efetivo','60','923456809','beatriz.nunes21@artemis.com','Faro','portuguesa','F','casada','ATLÂNTICO','00345678901234567910',5,'afastado','2024-01-19','2004-06-14',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(22,'Fernando Almeida',6,'efetivo','64','923456810','fernando.almeida22@artemis.com','Moxico','angolana','M','solteiro','BAI','00345678901234567911',5,'afastado','2025-01-15','2005-09-05',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(23,'Clara Marques',7,'efetivo','80','923456811','clara.marques23@artemis.com','Leiria','portuguesa','F','solteira','BPC','00345678901234567912',8,'ativo','2024-08-31','1995-01-12',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(24,'Ricardo Gomes',8,'efetivo','66','923456812','ricardo.gomes24@artemis.com','Cunene','angolana','M','casado','BFA','00345678901234567913',12,'ativo','2024-03-17','1994-02-15',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(25,'Diana Ferreira',1,'efetivo','73','923456813','diana.ferreira25@artemis.com','Viseu','portuguesa','F','solteira','SOL','00345678901234567914',6,'ativo','2025-03-31','1993-07-13',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(26,'Sérgio Ramos',2,'em formação','66','923456814','sergio.ramos26@artemis.com','Luanda','angolana','M','solteiro','BNI','00345678901234567915',14,'afastado','2025-03-14','1993-04-13',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(27,'Adriana Teixeira',3,'em formação','94','923456815','adriana.teixeira27@artemis.com','Porto','portuguesa','F','solteira','BCS','00345678901234567916',8,'ativo','2024-01-27','1993-10-25',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(28,'André Carvalho',4,'em formação','88','923456816','andre.carvalho28@artemis.com','Benguela','angolana','M','solteiro','ATLÂNTICO','00345678901234567917',7,'ativo','2025-02-26','1997-03-28',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(29,'Lúcia Cardoso',5,'eventual','60','923456817','lucia.cardoso29@artemis.com','Coimbra','portuguesa','F','casada','BAI','00345678901234567918',9,'ativo','2025-03-01','1998-09-29',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(30,'Vítor Pinto',6,'eventual','97','923456818','vitor.pinto30@artemis.com','Huambo','angolana','M','solteiro','BPC','00345678901234567919',15,'ativo','2024-02-26','1996-01-02',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(31,'Waldireny Adriano',7,'efetivo','84','923456819','waldireny.adriano@artemis.com','Luanda','angolana','F','solteira','BFA','00345678901234567920',7,'ativo','2025-09-05','2005-10-12',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(32,'Luís Gonzaga',1,'efetivo','68','923456820','luis.gonzaga@artemis.com','Huambo','angolana','M','casado','BPC','00345678901234567921',1,'afastado',NULL,NULL,NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(33,'Adelino Correia',3,'efetivo','71','924100001','adelino.correia33@artemis.com','Luanda','angolana','M','solteiro','BAI','00400000000000000033',3,'afastado','2023-03-10','1990-07-14',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(34,'Beatriz Lemos',5,'efetivo','91','924100002','beatriz.lemos34@artemis.com','Braga','portuguesa','F','solteira','BPC','00400000000000000034',5,'ativo','2022-11-05','1995-02-28',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(35,'Carlos Neto',7,'efetivo','61','924100003','carlos.neto35@artemis.com','Huambo','angolana','M','casado','BFA','00400000000000000035',7,'afastado','2023-06-20','1988-09-03',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(36,'Daniela Fonseca',4,'em formação','92','924100004','daniela.fonseca36@artemis.com','Lisboa','portuguesa','F','solteira','SOL','00400000000000000036',2,'ativo','2024-01-15','1998-04-11',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(37,'Emanuel Teixeira',8,'efetivo','97','924100005','emanuel.teixeira37@artemis.com','Benguela','angolana','M','casado','BNI','00400000000000000037',8,'afastado','2022-08-22','1987-12-19',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(38,'Fátima Araújo',8,'efetivo','68','924100006','fatima.araujo38@artemis.com','Porto','portuguesa','F','casada','BCS','00400000000000000038',1,'ativo','2021-05-17','1985-06-30',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(39,'Gabriel Mendes',8,'eventual','69','924100007','gabriel.mendes39@artemis.com','Malanje','angolana','M','solteiro','ATLÂNTICO','00400000000000000039',4,'ativo','2024-09-01','2000-01-22',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(40,'Helena Pires',3,'efetivo','84','924100008','helena.pires40@artemis.com','Coimbra','portuguesa','F','casada','BAI','00400000000000000040',6,'afastado','2022-03-14','1992-08-07',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(41,'Ilídio Machado',8,'efetivo','73','924100009','ilidio.machado41@artemis.com','Cabinda','angolana','M','divorciado','BPC','00400000000000000041',9,'ativo','2023-07-28','1983-03-15',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(42,'Joana Vieira',8,'efetivo','91','924100010','joana.vieira42@artemis.com','Faro','portuguesa','F','solteira','BFA','00400000000000000042',10,'ativo','2021-12-01','1996-11-09',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(43,'Kildare Afonso',3,'efetivo','97','924100011','kildare.afonso43@artemis.com','Luanda','angolana','M','casado','SOL','00400000000000000043',11,'ativo','2022-06-18','1989-05-25',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(44,'Lara Esteves',4,'em formação','68','924100012','lara.esteves44@artemis.com','Aveiro','portuguesa','F','solteira','BNI','00400000000000000044',12,'afastado','2025-02-10','2001-07-03',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(45,'Mário Cunha',8,'efetivo','71','924100013','mario.cunha45@artemis.com','Huíla','angolana','M','casado','BCS','00400000000000000045',13,'ativo','2020-10-05','1982-02-17',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(46,'Nádia Baptista',7,'efetivo','92','924100014','nadia.baptista46@artemis.com','Setúbal','portuguesa','F','casada','ATLÂNTICO','00400000000000000046',14,'ativo','2023-04-22','1991-10-14',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(47,'Orlando Simões',3,'efetivo','65','924100015','orlando.simoes47@artemis.com','Uíge','angolana','M','solteiro','BAI','00400000000000000047',15,'ativo','2022-09-30','1993-04-06',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(48,'Patrícia Moura',8,'efetivo','70','924100016','patricia.moura48@artemis.com','Braga','portuguesa','F','solteira','BPC','00400000000000000048',16,'ativo','2021-07-11','1994-08-21',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(49,'Quintino Leal',4,'efetivo','96','924100017','quintino.leal49@artemis.com','Bié','angolana','M','casado','BFA','00400000000000000049',17,'ativo','2023-01-19','1986-12-02',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(50,'Rita Guerreiro',8,'eventual','89','924100018','rita.guerreiro50@artemis.com','Leiria','portuguesa','F','solteira','SOL','00400000000000000050',18,'ativo','2024-11-07','1999-03-28',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(51,'Samuel Dias',9,'efetivo','97','924100019','samuel.dias51@artemis.com','Cuanza Norte','angolana','M','solteiro','BNI','00400000000000000051',19,'ativo','2022-05-23','1990-06-16',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(52,'Tatiana Rebelo',8,'efetivo','75','924100020','tatiana.rebelo52@artemis.com','Viseu','portuguesa','F','casada','BCS','00400000000000000052',20,'ativo','2021-08-14','1988-01-11',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(53,'Umberto Fragoso',2,'efetivo','67','924100021','umberto.fragoso53@artemis.com','Luanda','angolana','M','divorciado','ATLÂNTICO','00400000000000000053',3,'ativo','2023-10-02','1984-09-29',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(54,'Vanda Nascimento',5,'efetivo','89','924100022','vanda.nascimento54@artemis.com','Porto','portuguesa','F','solteira','BAI','00400000000000000054',5,'afastado','2022-04-16','1997-05-08',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(55,'Wilson Tavares',3,'em formação','63','924100023','wilson.tavares55@artemis.com','Moxico','angolana','M','solteiro','BPC','00400000000000000055',7,'ativo','2025-01-20','2002-11-17',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(56,'Xénia Carvalho',7,'efetivo','72','924100024','xenia.carvalho56@artemis.com','Coimbra','portuguesa','F','casada','BFA','00400000000000000056',9,'ativo','2021-11-08','1986-07-04',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(57,'Yannick Sousa',10,'efetivo','68','924100025','yannick.sousa57@artemis.com','Benguela','angolana','M','solteiro','SOL','00400000000000000057',11,'ativo','2023-08-15','1995-03-22',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(58,'Zara Monteiro',8,'efetivo','66','924100026','zara.monteiro58@artemis.com','Faro','portuguesa','F','solteira','BNI','00400000000000000058',13,'ativo','2022-07-29','1993-10-31',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(59,'Abílio Pereira',4,'efetivo','67','924100027','abilio.pereira59@artemis.com','Luanda','angolana','M','casado','BCS','00400000000000000059',2,'ativo','2020-12-03','1981-04-18',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(60,'Bruna Ferreira',6,'efetivo','76','924100028','bruna.ferreira60@artemis.com','Aveiro','portuguesa','F','casada','ATLÂNTICO','00400000000000000060',4,'ativo','2022-02-25','1990-02-14',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(61,'Celestino Amaral',9,'em formação','78','924100029','celestino.amaral61@artemis.com','Huambo','angolana','M','solteiro','BAI','00400000000000000061',6,'ativo','2025-03-05','2003-08-09',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(62,'Dora Henriques',4,'efetivo','63','924100030','dora.henriques62@artemis.com','Braga','portuguesa','F','solteira','BPC','00400000000000000062',8,'afastado','2021-06-17','1992-12-26',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(63,'Eugénio Brito',2,'efetivo','61','924100031','eugenio.brito63@artemis.com','Malanje','angolana','M','casado','BFA','00400000000000000063',10,'afastado','2023-05-11','1985-06-03',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(64,'Filipa Assunção',5,'efetivo','99','924100032','filipa.assuncao64@artemis.com','Lisboa','portuguesa','F','casada','SOL','00400000000000000064',12,'ativo','2021-09-22','1987-01-07',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(65,'Gonçalo Figueiredo',3,'efetivo','90','924100033','goncalo.figueiredo65@artemis.com','Cabinda','angolana','M','solteiro','BNI','00400000000000000065',14,'afastado','2022-10-14','1994-07-19',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(66,'Henriqueta Melo',7,'eventual','92','924100034','henriqueta.melo66@artemis.com','Setúbal','portuguesa','F','solteira','BCS','00400000000000000066',16,'ativo','2024-07-08','2000-09-15',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(67,'Isidoro Campos',10,'efetivo','90','924100035','isidoro.campos67@artemis.com','Huíla','angolana','M','casado','ATLÂNTICO','00400000000000000067',18,'ativo','2023-02-28','1983-11-24',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(68,'Júlia Andrade',8,'efetivo','72','924100036','julia.andrade68@artemis.com','Coimbra','portuguesa','F','casada','BAI','00400000000000000068',20,'afastado','2021-04-06','1989-04-30',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(69,'Lourenço Pacheco',4,'efetivo','73','924100037','lourenco.pacheco69@artemis.com','Uíge','angolana','M','solteiro','BPC','00400000000000000069',2,'ativo','2022-12-19','1996-02-05',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(70,'Margarida Loureiro',6,'efetivo','91','924100038','margarida.loureiro70@artemis.com','Viseu','portuguesa','F','casada','BFA','00400000000000000070',4,'afastado','2020-07-31','1984-08-13',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(71,'Nuno Borges',9,'efetivo','93','924100039','nuno.borges71@artemis.com','Luanda','angolana','M','divorciado','SOL','00400000000000000071',6,'ativo','2023-09-16','1981-03-08',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(72,'Olga Antunes',8,'em formação','90','924100040','olga.antunes72@artemis.com','Porto','portuguesa','F','solteira','BNI','00400000000000000072',8,'ativo','2025-02-28','2002-05-21',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(73,'Paulo Azevedo',2,'efetivo','73','924100041','paulo.azevedo73@artemis.com','Benguela','angolana','M','casado','BCS','00400000000000000073',10,'ativo','2022-01-10','1988-10-17',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(74,'Quirina Valente',5,'efetivo','78','924100042','quirina.valente74@artemis.com','Braga','portuguesa','F','solteira','ATLÂNTICO','00400000000000000074',12,'ativo','2021-10-24','1993-06-29',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(75,'Renato Brandão',3,'efetivo','67','924100043','renato.brandao75@artemis.com','Bié','angolana','M','solteiro','BAI','00400000000000000075',14,'ferias','2023-11-07','1991-01-16',NULL,NULL,'',NULL,'luanda',NULL,NULL,NULL,NULL),(76,'Susana Goulart',7,'efetivo','84','924100044','susana.goulart76@artemis.com','Leiria','portuguesa','F','casada','BPC','00400000000000000076',16,'ativo','2022-05-03','1986-09-04',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(77,'Tiago Matos',10,'efetivo','79','924100045','tiago.matos77@artemis.com','Cuanza Norte','angolana','M','solteiro','BFA','00400000000000000077',18,'ativo','2023-03-25','1997-07-11',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(78,'Ursula Freitas',8,'eventual','83','924100046','ursula.freitas78@artemis.com','Aveiro','portuguesa','F','solteira','SOL','00400000000000000078',20,'afastado','2024-08-19','1999-12-03',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(79,'Valentim Cruz',4,'efetivo','78','924100047','valentim.cruz79@artemis.com','Moxico','angolana','M','casado','BNI','00400000000000000079',3,'afastado','2021-02-08','1982-05-27',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(80,'Wanda Ribeiro',6,'efetivo','80','924100048','wanda.ribeiro80@artemis.com','Faro','portuguesa','F','casada','BCS','00400000000000000080',5,'ativo','2022-08-31','1990-11-08',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(81,'Xavier Domingues',9,'efetivo','66','924100049','xavier.domingues81@artemis.com','Luanda','angolana','M','solteiro','ATLÂNTICO','00400000000000000081',7,'afastado','2023-06-14','1995-04-24',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(82,'Yolanda Castelo',8,'efetivo','70','924100050','yolanda.castelo82@artemis.com','Lisboa','portuguesa','F','casada','BAI','00400000000000000082',3,'afastado','2020-11-29','1985-08-16',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(83,'Zeferino Alves',2,'em_formacao','95','924100051','zeferino.alves83@artemis.com','Huambo','angolana','M','solteiro','BPC','00400000000000000083',11,'afastado','2025-01-06','2001-02-19',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(84,'Amélia Rodrigues',5,'efetivo','80','924100052','amelia.rodrigues84@artemis.com','Coimbra','portuguesa','F','solteira','BFA','00400000000000000084',13,'afastado','2022-07-12','1992-09-07',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(85,'Bernardino Salomão',3,'efetivo','96','924100053','bernardino.salomao85@artemis.com','Cabinda','angolana','M','casado','SOL','00400000000000000085',15,'afastado','2021-03-17','1987-03-31',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(86,'Cecília Vasconcelos',7,'efetivo','98','924100054','cecilia.vasconcelos86@artemis.com','Braga','portuguesa','F','casada','BNI','00400000000000000086',17,'afastado','2021-08-03','1984-12-14',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(87,'Dinis Sampaio',1,'efetivo','60','924100055','dinis.sampaio87@artemis.com','Malanje','angolana','M','solteiro','BCS','00400000000000000087',19,'ativo','2023-04-09','1994-06-02',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(88,'Edite Carmo',8,'efetivo','73','924100056','edite.carmo88@artemis.com','Setúbal','portuguesa','F','solteira','ATLÂNTICO','00400000000000000088',2,'afastado','2022-11-21','1993-01-25',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(89,'Flávio Henrique',4,'efetivo','81','924100057','flavio.henrique89@artemis.com','Huíla','angolana','M','casado','BAI','00400000000000000089',4,'afastado','2021-05-28','1981-07-20',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(90,'Graça Pinheiro',6,'eventual','88','924100058','graca.pinheiro90@artemis.com','Viseu','portuguesa','F','casada','BPC','00400000000000000090',6,'afastado','2024-10-15','1998-03-12',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(91,'Hélder Queirós',9,'efetivo','96','924100059','helder.queiros91@artemis.com','Uíge','angolana','M','divorciado','BFA','00400000000000000091',8,'ativo','2022-09-07','1983-10-06',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(92,'Irene Machado',10,'efetivo','74','924100060','irene.machado92@artemis.com','Porto','portuguesa','F','solteira','SOL','00400000000000000092',10,'ativo','2023-12-18','1996-05-30',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(93,'Jacinto Ferreira',2,'efetivo','62','924100061','jacinto.ferreira93@artemis.com','Benguela','angolana','M','casado','BNI','00400000000000000093',12,'ativo','2021-01-13','1986-11-22',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(94,'Kátia Abreu',5,'em formação','70','924100062','katia.abreu94@artemis.com','Leiria','portuguesa','F','solteira','BCS','00400000000000000094',14,'ativo','2025-03-01','2000-08-18',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(95,'Leandro Faria',3,'efetivo','62','924100063','leandro.faria95@artemis.com','Luanda','angolana','M','solteiro','ATLÂNTICO','00400000000000000095',16,'ativo','2023-07-04','1992-02-09',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(96,'Mafalda Couto',7,'efetivo','82','924100064','mafalda.couto96@artemis.com','Aveiro','portuguesa','F','casada','BAI','00400000000000000096',18,'ativo','2020-09-25','1984-04-17',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(97,'Narciso Dinis',8,'efetivo','84','924100065','narciso.dinis97@artemis.com','Bié','angolana','M','casado','BPC','00400000000000000097',20,'afastado','2022-04-07','1980-06-26',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(98,'Olívia Mendonça',8,'efetivo','73','924100066','olivia.mendonca98@artemis.com','Braga','portuguesa','F','solteira','BFA','00400000000000000098',3,'ativo','2021-07-22','1991-09-14',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(99,'Plácido Carneiro',4,'efetivo','94','924100067','placido.carneiro99@artemis.com','Cuanza Norte','angolana','M','solteiro','SOL','00400000000000000099',5,'ativo','2023-10-31','1988-07-01',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(100,'Quintina Barros',6,'efetivo','68','924100068','quintina.barros100@artemis.com','Coimbra','portuguesa','F','casada','BNI','00400000000000000100',7,'afastado','2022-06-09','1989-03-23',NULL,NULL,NULL,NULL,'luanda',NULL,NULL,NULL,NULL),(101,'Edmar Leonardo',3,'efetivo','80','925640605','edmarleonardo@gmail.com','','angolana','M','solteiro','BAI','00401234786500000987',3,'ativo','2026-03-26','2007-04-16','Lubango','Bairro Heva, Palanca, Huíla','','006748983HA078','Huíla','',NULL,'Edmar Leonardo',NULL),(103,'Maria Cristina Dungula',4,'eventual','90','987000665','mariadungula@gmail.com','Luanda','angolana','F','solteira','BAI','0067553321',3,'ativo','2026-03-29','1999-07-22','Luanda','Rua da Dira','','090099176LN44','Luanda','AO09876524566',NULL,'Maria Cristina Dungula',NULL),(104,'Miriam Miguel',7,'efetivo','98','923555777','miriammiguel@gmail.com','Humpata','angolana','F','solteira','BPC','009878653210007888',6,'ativo','2026-04-01','2007-01-09','Humpata','Humpata, Rua Y','','090099235HA051','Huíla','AO0060000123455556',NULL,'Miriam Sindiquile Bioco Miguel',NULL);
/*!40000 ALTER TABLE `funcionarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `membros_equipas`
--

DROP TABLE IF EXISTS `membros_equipas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `membros_equipas` (
  `cod_membro` int NOT NULL AUTO_INCREMENT,
  `id_equipas` int NOT NULL,
  `f_id` int NOT NULL,
  `papel` varchar(45) NOT NULL,
  `data_entrada` date NOT NULL,
  `data_saida` date DEFAULT NULL,
  PRIMARY KEY (`cod_membro`),
  UNIQUE KEY `id_membro_equipa_UNIQUE` (`cod_membro`),
  KEY `id_equipas` (`id_equipas`),
  KEY `f_id` (`f_id`),
  CONSTRAINT `membros_equipas_ibfk_1` FOREIGN KEY (`id_equipas`) REFERENCES `equipas` (`id_equipas`),
  CONSTRAINT `membros_equipas_ibfk_2` FOREIGN KEY (`f_id`) REFERENCES `funcionarios` (`f_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `membros_equipas`
--

LOCK TABLES `membros_equipas` WRITE;
/*!40000 ALTER TABLE `membros_equipas` DISABLE KEYS */;
INSERT INTO `membros_equipas` VALUES (1,1,4,'Irrigação Matinal das 8 - 12','2026-03-15',NULL);
/*!40000 ALTER TABLE `membros_equipas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `planeament_ferias`
--

DROP TABLE IF EXISTS `planeament_ferias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `planeament_ferias` (
  `id_solicitacao` int NOT NULL AUTO_INCREMENT,
  `tipo_ausencia` varchar(20) NOT NULL,
  `data_inicio` date NOT NULL,
  `data_fim` date NOT NULL,
  `dias_uteis` int NOT NULL,
  `status` varchar(20) NOT NULL,
  `observacoes` longtext,
  `criado_em` datetime(6) NOT NULL,
  `atualizado_em` datetime(6) NOT NULL,
  `data_aprovacao` datetime(6) DEFAULT NULL,
  `aprovado_por_id` int DEFAULT NULL,
  `funcionario_id` int NOT NULL,
  PRIMARY KEY (`id_solicitacao`),
  KEY `planeament_ferias_aprovado_por_id_e68217cf_fk_funcionarios_f_id` (`aprovado_por_id`),
  KEY `planeament_ferias_funcionario_id_e37f4cbb_fk_funcionarios_f_id` (`funcionario_id`),
  CONSTRAINT `planeament_ferias_aprovado_por_id_e68217cf_fk_funcionarios_f_id` FOREIGN KEY (`aprovado_por_id`) REFERENCES `funcionarios` (`f_id`),
  CONSTRAINT `planeament_ferias_funcionario_id_e37f4cbb_fk_funcionarios_f_id` FOREIGN KEY (`funcionario_id`) REFERENCES `funcionarios` (`f_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `planeament_ferias`
--

LOCK TABLES `planeament_ferias` WRITE;
/*!40000 ALTER TABLE `planeament_ferias` DISABLE KEYS */;
INSERT INTO `planeament_ferias` VALUES (1,'maternidade','2026-03-30','2026-06-06',48,'aprovado','','2026-03-30 10:14:10.240769','2026-04-01 08:07:28.446798','2026-03-30 11:19:51.413806',NULL,3),(2,'ferias','2026-03-31','2026-04-07',6,'aprovado','Disse estar fatigado','2026-03-31 19:31:45.221037','2026-03-31 19:55:58.764491','2026-03-31 20:55:58.764304',NULL,101),(3,'maternidade','2026-04-08','2026-04-10',3,'aprovado','Está nos últimos dias','2026-04-08 15:48:08.848928','2026-04-08 15:55:14.906590','2026-04-08 16:55:14.906480',NULL,19),(4,'medica','2026-04-08','2026-04-09',2,'aprovado','Maculo','2026-04-08 16:21:25.455391','2026-04-08 16:21:36.250213','2026-04-08 17:21:36.250001',32,8),(5,'ferias','2026-04-13','2026-05-05',16,'aprovado','','2026-04-13 03:45:05.769781','2026-04-13 03:45:33.311073','2026-04-13 03:45:33.310862',NULL,75),(6,'ferias','2026-04-13','2026-05-05',16,'rejeitado','','2026-04-13 03:45:05.960433','2026-04-13 03:45:48.439602',NULL,NULL,75),(7,'maternidade','2026-04-13','2026-04-20',6,'pendente','','2026-04-13 04:07:57.596275','2026-04-13 04:07:57.596298',NULL,NULL,28);
/*!40000 ALTER TABLE `planeament_ferias` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `processo_seletivo`
--

DROP TABLE IF EXISTS `processo_seletivo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `processo_seletivo` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `etapa` varchar(30) NOT NULL,
  `resultado` varchar(20) NOT NULL,
  `data_agendada` datetime(6) DEFAULT NULL,
  `nota` decimal(4,2) DEFAULT NULL,
  `observacoes` longtext,
  `data_registo` datetime(6) NOT NULL,
  `avaliador_id` int DEFAULT NULL,
  `candidato_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `processo_seletivo_avaliador_id_5d1be3a7_fk_funcionarios_f_id` (`avaliador_id`),
  KEY `processo_seletivo_candidato_id_ecff2bb3_fk_candidatos_id` (`candidato_id`),
  CONSTRAINT `processo_seletivo_avaliador_id_5d1be3a7_fk_funcionarios_f_id` FOREIGN KEY (`avaliador_id`) REFERENCES `funcionarios` (`f_id`),
  CONSTRAINT `processo_seletivo_candidato_id_ecff2bb3_fk_candidatos_id` FOREIGN KEY (`candidato_id`) REFERENCES `candidatos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `processo_seletivo`
--

LOCK TABLES `processo_seletivo` WRITE;
/*!40000 ALTER TABLE `processo_seletivo` DISABLE KEYS */;
INSERT INTO `processo_seletivo` VALUES (1,'recepcao_candidatura','Reprovado','2026-04-03 00:00:00.000000',1.00,'Não tem Currículum','2026-04-03 08:26:38.453140',32,3),(2,'recepcao_candidatura','Reprovado','2026-04-03 00:00:00.000000',1.00,'Sem currículum','2026-04-03 08:27:10.374461',32,4),(3,'recepcao_candidatura','Aprovado','2026-04-03 00:00:00.000000',5.00,'Currículum promissor','2026-04-03 08:28:22.766560',32,7),(4,'analise_cv','Aprovado','2026-04-03 00:00:00.000000',5.00,'','2026-04-03 08:30:03.018890',32,7),(5,'entrevista_rh','Aprovado','2026-04-03 00:00:00.000000',5.00,'Boa fonética','2026-04-03 08:30:41.139641',32,7),(6,'entrevista_rh','Aprovado','2026-04-07 00:00:00.000000',5.00,'Gostei','2026-04-07 17:29:24.092299',32,7),(7,'teste_escrito','Aprovado','2026-04-07 00:00:00.000000',5.00,'','2026-04-07 17:30:36.209770',32,7),(8,'recepcao_candidatura','Aprovado','2026-04-07 00:00:00.000000',5.00,'','2026-04-07 20:23:48.705852',32,6),(9,'analise_cv','Aprovado','2026-04-07 00:00:00.000000',5.00,'','2026-04-07 20:24:49.932387',32,6),(10,'entrevista_rh','Aprovado','2026-04-07 00:00:00.000000',5.00,'','2026-04-07 20:25:16.379619',32,6),(11,'entrevista_tecnica','Aprovado','2026-04-07 00:00:00.000000',4.00,'','2026-04-07 20:25:34.323946',32,6),(12,'teste_escrito','Aprovado','2026-04-07 00:00:00.000000',5.00,'','2026-04-07 20:25:55.704048',32,6),(13,'teste_pratico','Aprovado','2026-04-07 00:00:00.000000',5.00,'','2026-04-07 20:26:11.142344',32,6),(14,'proposta','Aprovado','2026-04-07 00:00:00.000000',5.00,'','2026-04-07 20:26:30.278674',NULL,6),(15,'proposta','Aprovado','2026-04-07 00:00:00.000000',5.00,'','2026-04-07 20:26:47.231174',32,6),(16,'recepcao_candidatura','Reprovado','2026-04-07 00:00:00.000000',1.00,'Sem CV','2026-04-07 20:56:53.606977',32,2),(17,'recepcao_candidatura','Reprovado',NULL,0.00,'','2026-04-11 11:12:25.611571',NULL,1);
/*!40000 ALTER TABLE `processo_seletivo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `relatorios_relatorioagendado`
--

DROP TABLE IF EXISTS `relatorios_relatorioagendado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `relatorios_relatorioagendado` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nome` varchar(150) NOT NULL,
  `tipo` varchar(20) NOT NULL,
  `periodo` varchar(10) NOT NULL,
  `formato` varchar(10) NOT NULL,
  `ativo` tinyint(1) NOT NULL,
  `criado_em` datetime(6) NOT NULL,
  `atualizado` datetime(6) NOT NULL,
  `proxima_execucao` datetime(6) DEFAULT NULL,
  `criado_por_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `relatorios_relatorioagendado_criado_por_id_00ee4632_fk_users_id` (`criado_por_id`),
  CONSTRAINT `relatorios_relatorioagendado_criado_por_id_00ee4632_fk_users_id` FOREIGN KEY (`criado_por_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `relatorios_relatorioagendado`
--

LOCK TABLES `relatorios_relatorioagendado` WRITE;
/*!40000 ALTER TABLE `relatorios_relatorioagendado` DISABLE KEYS */;
INSERT INTO `relatorios_relatorioagendado` VALUES (1,'Vendas','vendas','diario','pdf',1,'2026-04-12 10:48:49.121030','2026-04-12 10:48:49.121073','2026-04-13 10:48:58.633684',2),(2,'RH','custom','mensal','pdf',1,'2026-04-12 10:49:36.571608','2026-04-12 10:49:36.571648','2026-05-12 10:49:52.922059',2),(3,'Vendas','vendas','diario','pdf',1,'2026-04-12 10:49:59.059648','2026-04-12 10:49:59.059700','2026-04-13 11:01:25.226937',2),(4,'Financeiro','financeiro','diario','pdf',1,'2026-04-12 10:50:00.173527','2026-04-12 10:50:00.173571','2026-04-13 10:50:12.312599',2),(5,'CRM','custom','diario','pdf',1,'2026-04-12 10:50:03.670500','2026-04-12 10:50:03.670540','2026-04-13 10:50:13.215549',2),(6,'RH','usuarios','diario','pdf',1,'2026-04-12 10:50:05.852936','2026-04-12 10:50:05.852980','2026-04-13 10:50:13.697813',2),(7,'Stock','custom','diario','pdf',1,'2026-04-12 10:50:05.819750','2026-04-12 10:50:05.819795','2026-04-13 10:50:14.665391',2),(8,'Executivo','custom','diario','pdf',1,'2026-04-12 10:50:06.200303','2026-04-12 10:50:06.200343','2026-04-13 10:50:14.070744',2),(9,'Financeiro','financeiro','diario','pdf',1,'2026-04-12 10:50:09.314870','2026-04-12 10:50:09.314912','2026-04-13 10:50:15.083758',2),(10,'Executivo','custom','diario','pdf',1,'2026-04-12 10:50:10.406163','2026-04-12 10:50:10.406200','2026-04-13 10:50:15.651307',2),(11,'Recurso humanos','custom','mensal','pdf',1,'2026-04-12 11:02:40.235837','2026-04-12 11:02:40.235936','2026-05-12 11:02:55.359691',2),(12,'Relatório de Vendas','vendas','mensal','pdf',1,'2026-04-12 11:03:25.372166','2026-04-12 11:03:25.372215','2026-05-12 11:03:26.016184',2),(13,'Relatório de Vendas','vendas','mensal','pdf',1,'2026-04-12 11:15:48.917839','2026-04-12 11:15:48.917878','2026-05-12 11:15:52.450767',2),(14,'Análise de RH','usuarios','mensal','pdf',1,'2026-04-12 11:16:32.935571','2026-04-12 11:16:32.935614','2026-05-12 11:16:33.674151',2);
/*!40000 ALTER TABLE `relatorios_relatorioagendado` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `relatorios_relatoriogerado`
--

DROP TABLE IF EXISTS `relatorios_relatoriogerado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `relatorios_relatoriogerado` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status` varchar(15) NOT NULL,
  `periodo_ref` varchar(50) NOT NULL,
  `mensagem_erro` longtext NOT NULL,
  `gerado_em` datetime(6) NOT NULL,
  `concluido_em` datetime(6) DEFAULT NULL,
  `agendamento_id` bigint DEFAULT NULL,
  `arquivo_path` varchar(500) NOT NULL,
  `nome_arquivo` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `relatorios_relatorio_agendamento_id_4df3e244_fk_relatorio` (`agendamento_id`),
  CONSTRAINT `relatorios_relatorio_agendamento_id_4df3e244_fk_relatorio` FOREIGN KEY (`agendamento_id`) REFERENCES `relatorios_relatorioagendado` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `relatorios_relatoriogerado`
--

LOCK TABLES `relatorios_relatoriogerado` WRITE;
/*!40000 ALTER TABLE `relatorios_relatoriogerado` DISABLE KEYS */;
INSERT INTO `relatorios_relatoriogerado` VALUES (1,'concluido','12/04/2026','','2026-04-12 10:48:55.975862','2026-04-12 10:48:58.117255',1,'',''),(2,'concluido','April/2026','','2026-04-12 10:49:39.879747','2026-04-12 10:49:41.885142',2,'',''),(3,'concluido','April/2026','','2026-04-12 10:49:46.807232','2026-04-12 10:49:50.687483',2,'',''),(4,'concluido','12/04/2026','','2026-04-12 10:50:11.210754','2026-04-12 10:50:11.528063',3,'',''),(5,'concluido','12/04/2026','','2026-04-12 10:50:11.815139','2026-04-12 10:50:12.105083',4,'',''),(6,'concluido','12/04/2026','','2026-04-12 10:50:12.782111','2026-04-12 10:50:13.083819',5,'',''),(7,'concluido','12/04/2026','','2026-04-12 10:50:13.389832','2026-04-12 10:50:13.605764',6,'',''),(8,'concluido','12/04/2026','','2026-04-12 10:50:13.918395','2026-04-12 10:50:13.982248',8,'',''),(9,'concluido','12/04/2026','','2026-04-12 10:50:14.173517','2026-04-12 10:50:14.419736',7,'',''),(10,'concluido','12/04/2026','','2026-04-12 10:50:14.821366','2026-04-12 10:50:15.036740',9,'',''),(11,'concluido','12/04/2026','','2026-04-12 10:50:15.294420','2026-04-12 10:50:15.401309',10,'',''),(12,'concluido','12/04/2026','','2026-04-12 10:50:15.928981','2026-04-12 10:50:16.071830',3,'',''),(13,'concluido','12/04/2026','','2026-04-12 11:01:22.851435','2026-04-12 11:01:24.628340',3,'',''),(14,'concluido','April/2026','','2026-04-12 11:02:41.447853','2026-04-12 11:02:42.630362',11,'',''),(15,'concluido','April/2026','','2026-04-12 11:02:55.001406','2026-04-12 11:02:55.290650',11,'',''),(16,'concluido','April/2026','','2026-04-12 11:03:25.532030','2026-04-12 11:03:25.911018',12,'',''),(17,'concluido','April/2026','','2026-04-12 11:15:50.031757','2026-04-12 11:15:50.755103',13,'',''),(18,'concluido','April/2026','','2026-04-12 11:16:33.026604','2026-04-12 11:16:33.499993',14,'','');
/*!40000 ALTER TABLE `relatorios_relatoriogerado` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stock_categoria`
--

DROP TABLE IF EXISTS `stock_categoria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stock_categoria` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `descricao` longtext NOT NULL,
  `prefixo` varchar(3) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stock_categoria`
--

LOCK TABLES `stock_categoria` WRITE;
/*!40000 ALTER TABLE `stock_categoria` DISABLE KEYS */;
INSERT INTO `stock_categoria` VALUES (1,'Produção Nacional','Frutas e insumos produzidos localmente em Angola',NULL);
/*!40000 ALTER TABLE `stock_categoria` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stock_fornecedor`
--

DROP TABLE IF EXISTS `stock_fornecedor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stock_fornecedor` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nome_empresa` varchar(200) NOT NULL,
  `contacto` varchar(50) NOT NULL,
  `email` varchar(254) NOT NULL,
  `tempo_entrega_dias` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `stock_fornecedor_chk_1` CHECK ((`tempo_entrega_dias` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stock_fornecedor`
--

LOCK TABLES `stock_fornecedor` WRITE;
/*!40000 ALTER TABLE `stock_fornecedor` DISABLE KEYS */;
INSERT INTO `stock_fornecedor` VALUES (1,'Ango-Agro Lda','+244 923 111 222','comercial@angoagro.ao',3),(2,'Quitutes Nacionais','924495879','quitutes@gmail.com',12);
/*!40000 ALTER TABLE `stock_fornecedor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stock_movimentacao`
--

DROP TABLE IF EXISTS `stock_movimentacao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stock_movimentacao` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `data` datetime(6) NOT NULL,
  `quantidade` int unsigned NOT NULL,
  `tipo` varchar(1) NOT NULL,
  `motivo` varchar(255) NOT NULL,
  `produto_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `stock_movimentacao_produto_id_278c094b_fk_stock_produto_id` (`produto_id`),
  CONSTRAINT `stock_movimentacao_produto_id_278c094b_fk_stock_produto_id` FOREIGN KEY (`produto_id`) REFERENCES `stock_produto` (`id`),
  CONSTRAINT `stock_movimentacao_chk_1` CHECK ((`quantidade` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stock_movimentacao`
--

LOCK TABLES `stock_movimentacao` WRITE;
/*!40000 ALTER TABLE `stock_movimentacao` DISABLE KEYS */;
INSERT INTO `stock_movimentacao` VALUES (1,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',1),(2,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',2),(3,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',3),(4,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',4),(5,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',5),(6,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',6),(7,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',7),(8,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',8),(9,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',9),(10,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',10),(11,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',11),(12,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',12),(13,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',13),(14,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',14),(15,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',15),(16,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',16),(17,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',17),(18,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',18),(19,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',19),(20,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',20),(21,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',21),(22,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',22),(23,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',23),(24,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',24),(25,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',25),(26,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',26),(27,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',27),(28,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',28),(29,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',29),(30,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',30),(31,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',31),(32,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',32),(33,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',33),(34,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',34),(35,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',35),(36,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',36),(37,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',37),(38,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',38),(39,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',39),(40,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',40),(41,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',41),(42,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',42),(43,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',43),(44,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',44),(45,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',45),(46,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',46),(47,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',47),(48,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',48),(49,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',49),(50,'2026-04-11 16:19:14.000000',500,'E','Inventário Inicial 2026',50),(51,'2026-04-12 18:08:30.000000',50,'E','Inventário Inicial 2026',51),(64,'2026-04-12 17:42:45.345436',1,'S','Perda',51);
/*!40000 ALTER TABLE `stock_movimentacao` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stock_produto`
--

DROP TABLE IF EXISTS `stock_produto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stock_produto` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `id_produto` varchar(50) NOT NULL,
  `nome` varchar(200) NOT NULL,
  `preco_custo` decimal(10,2) NOT NULL,
  `stock_minimo` int unsigned NOT NULL,
  `categoria_id` bigint DEFAULT NULL,
  `fornecedor_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_produto` (`id_produto`),
  KEY `stock_produto_categoria_id_231a8650_fk_stock_categoria_id` (`categoria_id`),
  KEY `stock_produto_fornecedor_id_e1bd179b_fk_stock_fornecedor_id` (`fornecedor_id`),
  CONSTRAINT `stock_produto_categoria_id_231a8650_fk_stock_categoria_id` FOREIGN KEY (`categoria_id`) REFERENCES `stock_categoria` (`id`),
  CONSTRAINT `stock_produto_fornecedor_id_e1bd179b_fk_stock_fornecedor_id` FOREIGN KEY (`fornecedor_id`) REFERENCES `stock_fornecedor` (`id`),
  CONSTRAINT `stock_produto_chk_1` CHECK ((`stock_minimo` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stock_produto`
--

LOCK TABLES `stock_produto` WRITE;
/*!40000 ALTER TABLE `stock_produto` DISABLE KEYS */;
INSERT INTO `stock_produto` VALUES (1,'LAR-001','Laranja Valência Especial',450.00,100,1,1),(2,'LAR-002','Laranja Baía do Dombe',500.00,100,1,1),(3,'LAR-003','Laranja Doce da Huíla',480.00,100,1,1),(4,'LAR-004','Sumo de Laranja Natural 5L',3500.00,20,1,1),(5,'LAR-005','Polpa de Laranja Congelada',1200.00,50,1,1),(6,'LAR-006','Laranja Lima Nacional',550.00,80,1,1),(7,'LAR-007','Sementes de Laranja Certificadas',2500.00,10,1,1),(8,'LAR-008','Mudas de Laranjeira Enxertada',4500.00,30,1,1),(9,'LAR-009','Casca de Laranja Seca (Granel)',800.00,40,1,1),(10,'LAR-010','Óleo Essencial de Laranja Benguela',7500.00,5,1,1),(11,'ADU-001','Ango-Adubo Crescimento Plus',15000.00,15,1,1),(12,'ADU-002','Super-Kwanza Fosfato',12500.00,15,1,1),(13,'ADU-003','Bio-Huambo Orgânico',8900.00,20,1,1),(14,'ADU-004','Ango-Azoto 20-10-10',18000.00,10,1,1),(15,'ADU-005','Fertilizante Líquido Calulo',6500.00,25,1,1),(16,'ADU-006','Calcário Agrícola da Chela',4200.00,50,1,1),(17,'ADU-007','Ango-Potássio Especial',14700.00,12,1,1),(18,'ADU-008','Adubo de Curral Biológico',3500.00,100,1,1),(19,'ADU-009','Micro-Nutrientes Catumbela',9800.00,10,1,1),(20,'ADU-010','Ango-Raiz Estimulante',11000.00,8,1,1),(21,'PRG-001','Anti-Praga Kwanza Sul',5600.00,20,1,1),(22,'PRG-002','Fungicida Matala',7200.00,15,1,1),(23,'PRG-003','Inseticida Citrinos Bengo',6800.00,15,1,1),(24,'PRG-004','Herbicida Limpa-Pomar',8500.00,10,1,1),(25,'PRG-005','Isco para Moscas da Fruta',3200.00,50,1,1),(26,'PRG-006','Gel de Proteção Cicatrizante',2900.00,20,1,1),(27,'PRG-007','Repelente Orgânico Namibe',4100.00,15,1,1),(28,'PRG-008','Óleo de Verão Anti-Cochonilha',5400.00,10,1,1),(29,'PRG-009','Enxofre Agrícola em Pó',3800.00,30,1,1),(30,'PRG-010','Armadilha Delta para Citrinos',1500.00,100,1,1),(31,'EQU-001','Caixa Plástica Ventilada 20kg',4500.00,200,1,1),(32,'EQU-002','Sacos de Rede para Laranjas (100un)',2800.00,50,1,1),(33,'EQU-003','Tesoura de Poda Profissional',9500.00,5,1,1),(34,'EQU-004','Pulverizador Costal 20L',25000.00,3,1,1),(35,'EQU-005','Luvas de Proteção para Colheita',1800.00,40,1,1),(36,'EQU-006','Escadote de Alumínio Agrícola',42000.00,2,1,1),(37,'EQU-007','Balde de Colheita Reforçado',3200.00,25,1,1),(38,'EQU-008','Medidor de pH do Solo',12000.00,2,1,1),(39,'EQU-009','Termómetro de Solo Digital',8500.00,3,1,1),(40,'EQU-010','Cesta de Vime Tradicional',5000.00,15,1,1),(41,'CON-001','Fio de Ráfia para Atadura',1200.00,100,1,1),(42,'CON-002','Etiquetas Autocolantes Pomar',900.00,500,1,1),(43,'CON-003','Paletes de Madeira Reforçada',7500.00,40,1,1),(44,'CON-004','Filme Estirável Industrial',6200.00,10,1,1),(45,'CON-005','Detergente para Lavagem de Fruta',4800.00,12,1,1),(46,'CON-006','Cera de Polimento para Citrinos',13500.00,5,1,1),(47,'CON-007','Caixa de Cartão Exportação',1100.00,1000,1,1),(48,'CON-008','Fita Adesiva Fruta de Angola',850.00,30,1,1),(49,'CON-009','Papel de Seda para Embalagem',2400.00,20,1,1),(50,'CON-010','Kit de Primeiros Socorros Campo',15600.00,5,1,1),(51,'FRU-001','Caixas de Tangerina XXL',500.00,50,1,1);
/*!40000 ALTER TABLE `stock_produto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `f_id` int DEFAULT NULL,
  `nivel` varchar(20) NOT NULL,
  `tipo` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `f_id` (`f_id`),
  CONSTRAINT `users_f_id_efa1c0eb_fk_funcionarios_f_id` FOREIGN KEY (`f_id`) REFERENCES `funcionarios` (`f_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'pbkdf2_sha256$1000000$RaMvsS9Mt8SmxvsCMjcINK$zrNddlZPOPGWtePZuKXfRgeTMxq/BeLAI9LXVc8XnOw=','2026-04-12 16:19:30.376743',1,'gylmiguel07@gmail.com','Gililson','Miguel','gylmiguel07@gmail.com',1,1,'2026-03-02 12:21:38.000000',NULL,'supervisor','Programador'),(2,'pbkdf2_sha256$1000000$zPaUeBPbiTdsWPBbMogqES$yC5P1Bqi5T3IkRTNfZ1HHCMgZWRvcFG0D3Z2up5DRD4=','2026-04-13 03:13:37.433660',0,'alcides@dev.com','Alcides','Nolasco','cyberalcides@gmail.com',0,1,'2026-03-04 13:27:24.000000',NULL,'supervisor','Programador'),(3,'pbkdf2_sha256$1000000$dJt25RAY3EHngrdCxX3c6x$0emaSf9Qf1W7pe34E5qq1fYPdsK2p4AAeXUHdIO/6LM=','2026-04-13 06:07:55.916335',0,'luisgonzaga@gmail.com','Luís','Gonzaga','l9974000@gmail.com',1,1,'2026-03-09 14:51:13.000000',32,'supervisor','admin'),(4,'pbkdf2_sha256$1000000$skQRJCPnQc1wJ3OMUreNqF$rPjT7BLdMKSmpbHhR6N9V+Y+DW4E5TzUe7J5/pu4Kjw=','2026-04-13 03:51:26.938971',0,'erivaniotiago@gmail.com','Erivânio','Tiago','erivaniotiago@gmail.com',0,1,'2026-03-09 14:53:09.000000',4,'operario','stock'),(5,'pbkdf2_sha256$1000000$grXOsNRdPqHIv72U4EnLhR$8MhKDPJ/sQ5mxxoyUbN5vy8yt70SWcydruGGZGTBtJw=','2026-04-13 03:52:13.359447',0,'waldirenylua@gmail.com','Waldireny','Adriano','Waldirenylua@gmail.com',0,1,'2026-03-09 14:54:18.000000',31,'operario','rh');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_groups`
--

DROP TABLE IF EXISTS `users_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `users_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_groups_users_id_group_id_83a49e68_uniq` (`users_id`,`group_id`),
  KEY `users_groups_group_id_2f3517aa_fk_auth_group_id` (`group_id`),
  CONSTRAINT `users_groups_group_id_2f3517aa_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `users_groups_users_id_1e682706_fk_users_id` FOREIGN KEY (`users_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_groups`
--

LOCK TABLES `users_groups` WRITE;
/*!40000 ALTER TABLE `users_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users_user_permissions`
--

DROP TABLE IF EXISTS `users_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `users_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `users_user_permissions_users_id_permission_id_d7a00931_uniq` (`users_id`,`permission_id`),
  KEY `users_user_permissio_permission_id_6d08dcd2_fk_auth_perm` (`permission_id`),
  CONSTRAINT `users_user_permissio_permission_id_6d08dcd2_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `users_user_permissions_users_id_e1ed60a2_fk_users_id` FOREIGN KEY (`users_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users_user_permissions`
--

LOCK TABLES `users_user_permissions` WRITE;
/*!40000 ALTER TABLE `users_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `users_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `utilizadores_utilizador`
--

DROP TABLE IF EXISTS `utilizadores_utilizador`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `utilizadores_utilizador` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `foto` varchar(100) DEFAULT NULL,
  `telefone` varchar(20) NOT NULL,
  `tipo` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `utilizadores_utilizador`
--

LOCK TABLES `utilizadores_utilizador` WRITE;
/*!40000 ALTER TABLE `utilizadores_utilizador` DISABLE KEYS */;
/*!40000 ALTER TABLE `utilizadores_utilizador` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `utilizadores_utilizador_groups`
--

DROP TABLE IF EXISTS `utilizadores_utilizador_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `utilizadores_utilizador_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `utilizador_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `utilizadores_utilizador__utilizador_id_group_id_f1238dc8_uniq` (`utilizador_id`,`group_id`),
  KEY `utilizadores_utiliza_group_id_fe9b110e_fk_auth_grou` (`group_id`),
  CONSTRAINT `utilizadores_utiliza_group_id_fe9b110e_fk_auth_grou` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `utilizadores_utiliza_utilizador_id_05c50d4c_fk_utilizado` FOREIGN KEY (`utilizador_id`) REFERENCES `utilizadores_utilizador` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `utilizadores_utilizador_groups`
--

LOCK TABLES `utilizadores_utilizador_groups` WRITE;
/*!40000 ALTER TABLE `utilizadores_utilizador_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `utilizadores_utilizador_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `utilizadores_utilizador_user_permissions`
--

DROP TABLE IF EXISTS `utilizadores_utilizador_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `utilizadores_utilizador_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `utilizador_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `utilizadores_utilizador__utilizador_id_permission_8b49f421_uniq` (`utilizador_id`,`permission_id`),
  KEY `utilizadores_utiliza_permission_id_7b42356d_fk_auth_perm` (`permission_id`),
  CONSTRAINT `utilizadores_utiliza_permission_id_7b42356d_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `utilizadores_utiliza_utilizador_id_c1a5533f_fk_utilizado` FOREIGN KEY (`utilizador_id`) REFERENCES `utilizadores_utilizador` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `utilizadores_utilizador_user_permissions`
--

LOCK TABLES `utilizadores_utilizador_user_permissions` WRITE;
/*!40000 ALTER TABLE `utilizadores_utilizador_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `utilizadores_utilizador_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `vagas`
--

DROP TABLE IF EXISTS `vagas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `vagas` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `titulo` varchar(100) NOT NULL,
  `descricao` longtext NOT NULL,
  `requisitos` longtext NOT NULL,
  `num_vagas` int unsigned NOT NULL,
  `salario_oferecido` decimal(12,2) DEFAULT NULL,
  `tipo` varchar(20) NOT NULL,
  `estado` varchar(20) NOT NULL,
  `data_abertura` date NOT NULL,
  `data_limite` date DEFAULT NULL,
  `cargo_id` int NOT NULL,
  `criado_por_id` bigint DEFAULT NULL,
  `departamento_id` int NOT NULL,
  `num_candidaturas` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `vagas_cargo_id_803ad701_fk_cargos_id_cargo` (`cargo_id`),
  KEY `vagas_criado_por_id_34c41228_fk_users_id` (`criado_por_id`),
  KEY `vagas_departamento_id_1b00a166_fk_departamentos_id_dpt` (`departamento_id`),
  CONSTRAINT `vagas_cargo_id_803ad701_fk_cargos_id_cargo` FOREIGN KEY (`cargo_id`) REFERENCES `cargos` (`id_cargo`),
  CONSTRAINT `vagas_criado_por_id_34c41228_fk_users_id` FOREIGN KEY (`criado_por_id`) REFERENCES `users` (`id`),
  CONSTRAINT `vagas_departamento_id_1b00a166_fk_departamentos_id_dpt` FOREIGN KEY (`departamento_id`) REFERENCES `departamentos` (`id_dpt`),
  CONSTRAINT `vagas_chk_1` CHECK ((`num_vagas` >= 0)),
  CONSTRAINT `vagas_chk_2` CHECK ((`num_candidaturas` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `vagas`
--

LOCK TABLES `vagas` WRITE;
/*!40000 ALTER TABLE `vagas` DISABLE KEYS */;
INSERT INTO `vagas` VALUES (1,'Gerente de Produção','Responsável por planejar, coordenar e supervisionar todas as atividades de produção agrícola, garantindo o uso eficiente de recursos, o cumprimento de metas de produtividade e a qualidade das culturas. Atua na gestão de equipes de campo, no controle de insumos, na implementação de boas práticas agrícolas e no acompanhamento de indicadores de desempenho. Também colabora no planejamento de safras, manutenção de equipamentos e no cumprimento das normas de segurança e sustentabilidade.','Formação em Agronomia, Engenharia Agrícola ou áreas relacionadas\r\n\r\nExperiência em gestão de produção agrícola\r\n\r\nConhecimento em planejamento de safra, manejo de culturas e gestão de equipes\r\n\r\nBoa capacidade de organização, liderança e tomada de decisão',1,250000.00,'interno','aberta','2026-03-15',NULL,1,1,2,1),(2,'Vaga para técnico de irrigação','Responsável pela instalação, operação e manutenção de sistemas de irrigação, garantindo o fornecimento adequado de água às culturas e o uso eficiente dos recursos hídricos. Atua no monitoramento do funcionamento de bombas, tubulações, válvulas e aspersores, realizando ajustes e reparos quando necessário. Também acompanha a programação de irrigação de acordo com as necessidades das culturas e as condições climáticas.','Formação técnica em Agricultura, Irrigação, Agronomia ou áreas relacionadas\r\n\r\nExperiência com sistemas de irrigação (aspersão, gotejamento ou pivô)\r\n\r\nConhecimentos básicos de manutenção de equipamentos hidráulicos\r\n\r\nCapacidade de organização, trabalho em campo e resolução de problemas',3,50000.00,'interno','aberta','2026-03-15',NULL,3,1,3,2),(3,'Vaga Para Técnico de Refrigeração','Especialista em Refrigeração Agrícola responsável pela instalação, manutenção e otimização de sistemas de refrigeração aplicados à conservação de produtos agrícolas. Atua no controle de temperatura e umidade, garantindo a qualidade e durabilidade dos alimentos pós-colheita. Deve possuir conhecimentos técnicos em equipamentos frigoríficos, diagnóstico de falhas e eficiência energética, além de capacidade para trabalhar em campo e oferecer soluções práticas ao setor agrícola.\r\n','Requisitos para Especialista em Refrigeração Agrícola:\r\n\r\nFormação técnica ou superior em Refrigeração, Climatização, Mecânica ou áreas afins\r\n\r\nExperiência comprovada em sistemas de refrigeração (preferencialmente no setor agrícola)\r\n\r\nConhecimento em instalação, manutenção preventiva e corretiva de equipamentos frigoríficos\r\n\r\nNoções de conservação pós-colheita (frutas, hortícolas, etc.)\r\n\r\nCapacidade de diagnóstico e resolução de falhas técnicas\r\n\r\nConhecimentos básicos de eletricidade e sistemas de controlo\r\n\r\nFamiliaridade com normas de segurança e eficiência energética\r\n\r\nDisponibilidade para trabalhar em campo e realizar deslocações\r\n\r\nBoa capacidade de organização e gestão de tempo\r\n\r\nEspírito de equipa e proatividade\r\n\r\nCarta de condução (preferencial)',15,60000.00,'interno','aberta','2026-03-17',NULL,6,1,6,12),(4,'Vaga para Acessor de Recursos Humanos','Profissional responsável por apoiar a gestão de pessoas dentro da organização, atuando em processos de recrutamento e seleção, integração de colaboradores, gestão de desempenho e desenvolvimento organizacional. Contribui para a implementação de políticas de recursos humanos, promove um bom clima organizacional e assegura o cumprimento das normas laborais.','Formação em Recursos Humanos, Psicologia, Administração ou áreas afins\r\n\r\nExperiência prévia na área de RH (recrutamento, treinamento ou gestão de pessoal)\r\n\r\nConhecimento básico da legislação laboral\r\n\r\nBoa capacidade de comunicação e relacionamento interpessoal\r\n\r\nOrganização, ética e confidencialidade\r\n\r\nCapacidade de trabalhar em equipa e sob pressão\r\n\r\nDomínio de ferramentas informáticas (Excel, Word, sistemas de RH)\r\n\r\nEspírito analítico e atenção aos detalhes\r\n\r\nProatividade e capacidade de resolução de problemas',2,250000.00,'interno','encerrada','2026-03-17','2026-04-30',10,1,10,2),(5,'Assistente Administrativo para os Recursos Humanos','Assistente para ajudar O pessoal do Rh','Escolaridade elevada.\r\nFaculdade Concluída\r\nCarta de condução',2,250000.00,'externo','aberta','2026-03-30','2026-04-09',10,1,10,1);
/*!40000 ALTER TABLE `vagas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'artemis_db'
--

--
-- Dumping routines for database 'artemis_db'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-13  8:42:17
