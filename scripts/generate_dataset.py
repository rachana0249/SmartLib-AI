#!/usr/bin/env python3
"""
SmartLib AI - Expanded Comprehensive Academic Catalog Generator
Generates 320 high-quality academic learning resources across 8 STEM faculties.
Guarantees 35-45 books per domain across all difficulty levels (Beginner, Intermediate, Advanced)
and resource types (Textbook, Reference Book, Guide, Handbook, Lab Manual),
ensuring robust multi-attribute filtering, rich search matches, and zero 1-2 book starvation.
"""

import csv
import os

def load_base_catalog():
    # Load existing 125 entries if available to preserve benchmark ground truth
    csv_path = os.path.join("data", "library_resources.csv")
    base_entries = []
    if os.path.exists(csv_path):
        with open(csv_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Normalize Software Engineering subject into Computer Science
                if row.get("subject") == "Software Engineering":
                    row["subject"] = "Computer Science"
                base_entries.append(row)
                if len(base_entries) >= 125:
                    break
    return base_entries

# Domain templates for extensive catalog expansion to 320+ books
ADDITIONAL_DOMAINS_DATA = [
    # --- Computer Science ---
    ("Computer Science", "Algorithms & Data Structures", "Textbook", "Beginner",
     "Algorithms in a Nutshell", "George T. Heineman, Gary Pollice, Stanley Selkow",
     "Practical algorithms reference focusing on implementation and performance rather than rigorous mathematics. Covers sorting, searching, computational geometry, graph algorithms, and spatial indexes with code in C, C++, and Java.",
     "algorithms, data structures, sorting, binary search, graph algorithms, computational geometry, asymptotic notation",
     2016, "2nd Edition", "CS-Floor-2-A5", 6, 4, 4.6, 210, "Algorithms, Practical Reference"),

    ("Computer Science", "Algorithms & Data Structures", "Handbook", "Intermediate",
     "The Algorithm Design Manual", "Steven S. Skiena",
     "Widely acclaimed handbook serving as both a textbook and an algorithmic war-story field guide. Details catalog of algorithmic problems, dynamic programming, backtracking, heuristic search, and NP-complete reductions.",
     "algorithms, dynamic programming, skiena, algorithm design, graph algorithms, backtracking, heuristics",
     2020, "3rd Edition", "CS-Floor-2-A6", 7, 3, 4.9, 320, "Skiena, Algorithm Design, Essential"),

    ("Computer Science", "Algorithms & Data Structures", "Lab Manual", "Beginner",
     "Data Structures Laboratory Practice Manual", "G. A. Vijayalakshmi Pai",
     "Hands-on university laboratory workbook with step-by-step programming assignments in C and Python. Covers linked lists, binary search trees, AVL tree rotations, Dijkstra shortest paths, and minimum spanning trees.",
     "data structures, lab manual, programming exercises, c programming, avl trees, linked lists, graphs",
     2021, "2nd Edition", "CS-Floor-2-A7", 10, 8, 4.5, 190, "Lab Manual, Coursework"),

    ("Computer Science", "Algorithms & Data Structures", "Reference Book", "Advanced",
     "Purely Functional Data Structures", "Chris Okasaki",
     "Pioneering reference on implementing data structures in functional languages. Explores persistent data structures, lazy evaluation, amortized analysis, binomial heaps, red-black trees, and catenable lists.",
     "functional programming, data structures, persistent data structures, red-black trees, amortization, okasaki",
     1999, "1st Edition", "CS-Floor-2-A8", 4, 2, 4.8, 145, "Functional Data Structures, Advanced"),

    ("Computer Science", "Operating Systems", "Guide", "Beginner",
     "Linux Command Line and Shell Scripting Bible", "Richard Blum, Christine Bresnahan",
     "Comprehensive practical tutorial on Linux environments, bash scripting, file system hierarchy, process management, sed and gawk stream editing, and automated system administration.",
     "linux, shell scripting, bash, operating systems, sysadmin, command line, sed, awk, terminal",
     2021, "4th Edition", "CS-Floor-2-B5", 8, 5, 4.7, 340, "Linux, Shell Scripting"),

    ("Computer Science", "Operating Systems", "Lab Manual", "Intermediate",
     "Operating Systems Lab: Kernel Programming with xv6", "M. Frans Kaashoek, Robert Morris",
     "Practical hands-on lab guide exploring the xv6 teaching operating system. Step-by-step exercises on implementing system calls, process scheduling, page tables, memory allocators, and basic file systems.",
     "operating systems, xv6, kernel programming, system calls, page tables, memory management, lab manual",
     2022, "MIT OpenCourseWare Edition", "CS-Floor-2-B6", 6, 4, 4.9, 230, "OS Lab, xv6, Kernel"),

    ("Computer Science", "Operating Systems", "Reference Book", "Advanced",
     "Understanding the Linux Kernel", "Daniel P. Bovet, Marco Cesati",
     "In-depth architectural reference on the Linux kernel internals. Detailed breakdown of memory addressing, interrupt handling, process switching, kernel synchronization, block device drivers, and ext3/ext4 filesystems.",
     "linux kernel, kernel architecture, memory management, interrupts, drivers, virtual memory, scheduling",
     2005, "3rd Edition", "CS-Floor-2-B7", 5, 2, 4.8, 180, "Kernel Internals, Advanced OS"),

    ("Computer Science", "Database Systems", "Textbook", "Beginner",
     "Database Design for Mere Mortals", "Michael J. Hernandez",
     "Approachable, common-sense guide to relational database design without overwhelming theory. Covers entity-relationship modeling, table keys, normalization rules, and defining integrity constraints.",
     "database design, relational model, normalization, er diagrams, sql, database fundamentals",
     2020, "4th Edition", "CS-Floor-2-C7", 7, 5, 4.6, 260, "Database Design, Beginner"),

    ("Computer Science", "Database Systems", "Lab Manual", "Beginner",
     "SQL and Relational Database Systems Lab Workbook", "Abraham Silberschatz, S. Sudarshan",
     "Structured laboratory manual featuring PostgreSQL and MySQL exercises. Covers complex joins, nested subqueries, views, triggers, stored procedures, transaction isolation levels, and ACID property verification.",
     "sql lab, database lab, postgresql, queries, transactions, triggers, stored procedures, acid",
     2021, "Lab Edition", "CS-Floor-2-C8", 9, 6, 4.7, 240, "Lab Manual, SQL Hands-on"),

    ("Computer Science", "Database Systems", "Handbook", "Intermediate",
     "High Performance MySQL: Optimization, Backups, and Replication", "Silvia Botros, Jeremy Tinley",
     "Industry handbook for optimizing database performance. Explores query profiling, B-tree index design, storage engine tuning (InnoDB), read replicas, high availability clustering, and backup strategies.",
     "mysql, database performance, query optimization, indexing, b-trees, replication, innodb, scalability",
     2021, "4th Edition", "CS-Floor-2-C9", 5, 3, 4.7, 195, "Database Performance, MySQL"),

    ("Computer Science", "Distributed Systems", "Textbook", "Intermediate",
     "Distributed Systems: Principles and Paradigms", "Andrew S. Tanenbaum, Maarten van Steen",
     "Core university textbook on modern distributed systems. Covers communication protocols (RPC, RMI), processes and virtualization, naming, clock synchronization, Lamport timestamps, distributed mutual exclusion, and replication.",
     "distributed systems, tanenbaum, rpc, clock synchronization, consensus, fault tolerance, replication",
     2023, "4th Edition", "CS-Floor-2-D5", 7, 4, 4.8, 270, "Distributed Systems Core"),

    ("Computer Science", "Computer Networks", "Guide", "Beginner",
     "TCP/IP Illustrated: The Protocols", "W. Richard Stevens, Kevin R. Fall",
     "The definitive guide to the TCP/IP suite. Clear packet-level explanations of ARP, IPv4, IPv6, ICMP, UDP, TCP three-way handshakes, sliding windows, congestion control, and DNS.",
     "tcp/ip, computer networks, packet analysis, stevens, networking protocols, routing, sockets",
     2011, "2nd Edition", "CS-Floor-2-C10", 6, 3, 4.9, 290, "Networking Classic, Stevens"),

    ("Computer Science", "Computer Networks", "Lab Manual", "Intermediate",
     "Computer Networks Simulation and Wireshark Lab Guide", "James F. Kurose, Keith W. Ross",
     "Interactive laboratory workbook for packet dissection using Wireshark and network emulation with Mininet. Guided experiments on HTTP caching, TCP throughput, router queues, and DNS latency.",
     "wireshark, network lab, packet trace, mininet, tcp, udp, dns, router simulation, lab manual",
     2022, "Companion Lab Manual", "CS-Floor-2-C11", 8, 6, 4.8, 230, "Networking Lab, Wireshark"),

    ("Computer Science", "Software Engineering", "Textbook", "Intermediate",
     "Software Engineering: A Practitioner's Approach", "Roger S. Pressman, Bruce R. Maxim",
     "The standard university treatise on software engineering lifecycles. Details Agile methodologies (Scrum, Kanban), software requirements engineering, architectural modeling (UML), formal verification, and quality metrics.",
     "software engineering, pressman, agile, scrum, uml, software testing, requirements engineering, sdlc",
     2019, "9th Edition", "SWE-Floor-2-A3", 9, 5, 4.6, 310, "Software Engineering Standard"),

    ("Computer Science", "Software Engineering", "Lab Manual", "Beginner",
     "Full-Stack Web Engineering Lab Project Manual", "Robin Wieruch, Kyle Simpson",
     "Comprehensive undergraduate laboratory guide for building secure, testable web services. Covers Node.js, Express, REST APIs, React components, state management, and continuous integration pipelines.",
     "web engineering, lab manual, rest api, react, node.js, express, testing, frontend, backend",
     2023, "1st Edition", "SWE-Floor-2-B5", 8, 5, 4.7, 210, "Web Engineering Lab"),

    # --- Artificial Intelligence & Data Science ---
    ("Artificial Intelligence & Data Science", "Machine Learning", "Handbook", "Intermediate",
     "Approaching (Almost) Any Machine Learning Problem", "Abhishek Thakur",
     "Hands-on tactical handbook for competitive machine learning and practical modeling. Covers cross-validation schemes, tabular feature engineering, categorical embeddings, text classification, and hyperparameter tuning.",
     "machine learning, feature engineering, kaggle, cross validation, scikit-learn, tabular data, applied ml",
     2020, "1st Edition", "AI-Floor-3-A7", 6, 3, 4.8, 240, "Applied ML, Competitive Modeling"),

    ("Artificial Intelligence & Data Science", "Machine Learning", "Lab Manual", "Beginner",
     "Machine Learning Laboratory Manual: Python & Scikit-Learn", "Aurélien Géron, Jake VanderPlas",
     "Step-by-step practical laboratory workbook with complete Python code for implementing regression, decision trees, random forests, k-means clustering, support vector machines, and model evaluation metrics.",
     "machine learning lab, python, scikit-learn, lab exercises, random forest, regression, clustering, lab manual",
     2022, "University Lab Series", "AI-Floor-3-A8", 11, 8, 4.8, 290, "ML Lab, Python Lab"),

    ("Artificial Intelligence & Data Science", "Machine Learning", "Reference Book", "Advanced",
     "The Elements of Statistical Learning: Data Mining, Inference, and Prediction", "Trevor Hastie, Robert Tibshirani, Jerome Friedman",
     "The legendary benchmark reference on modern machine learning theory. In-depth mathematical treatment of generalized additive models, boosting (AdaBoost, gradient boosting), kernel smoothing, neural networks, and random forests.",
     "statistical learning, hastie, tibshirani, machine learning theory, boosting, support vector machines, splines",
     2009, "2nd Edition", "AI-Floor-3-A9", 6, 2, 5.0, 380, "Statistical Learning Bible, Stanford"),

    ("Artificial Intelligence & Data Science", "Deep Learning", "Textbook", "Beginner",
     "Deep Learning with Python", "François Chollet",
     "Written by the author of Keras, this book offers an intuitive introduction to deep learning. Covers neural network fundamentals, computer vision with CNNs, text processing with recurrent networks, and generative models.",
     "deep learning, keras, chollet, python, convolutional networks, neural networks, computer vision, beginner deep learning",
     2021, "2nd Edition", "AI-Floor-3-B8", 8, 4, 4.9, 360, "Keras, Chollet, Essential"),

    ("Artificial Intelligence & Data Science", "Deep Learning", "Lab Manual", "Intermediate",
     "Deep Learning Laboratory Experiments with PyTorch", "Eli Stevens, Luca Antiga",
     "Undergraduate lab manual guiding students through building custom neural network architectures in PyTorch. Includes tensor operations, autograd verification, CNN transfer learning, and LSTM sequence modeling.",
     "deep learning lab, pytorch, autograd, cnn, lab manual, transfer learning, tensors, neural networks",
     2023, "Lab Guide Edition", "AI-Floor-3-B9", 7, 5, 4.7, 215, "PyTorch Lab, Neural Networks"),

    ("Artificial Intelligence & Data Science", "Deep Learning", "Reference Book", "Advanced",
     "Generative Models and Diffusion Architectures", "David Foster, Ian Goodfellow",
     "Advanced research monograph exploring mathematical foundations of score-based diffusion models, denoising probabilistic models (DDPM), Latent Diffusion, and classifier-free guidance for multimodal generation.",
     "diffusion models, generative ai, ddpm, score-based models, generative adversarial networks, latent diffusion",
     2024, "1st Edition", "AI-Floor-3-B10", 5, 2, 4.8, 160, "Generative AI, Diffusion Models"),

    ("Artificial Intelligence & Data Science", "Natural Language Processing", "Guide", "Beginner",
     "Practical Natural Language Processing: A Comprehensive Guide to Building Real-World NLP Systems", "Sowmya Vajjala, Bodhisattwa Majumder, Anuj Gupta, Harshit Surana",
     "End-to-end industrial guide covering text extraction, preprocessing, tokenization, TF-IDF, Word2Vec, spaCy pipelines, named entity recognition (NER), text search ranking, and production deployment.",
     "nlp, natural language processing, tf-idf, spacy, text classification, search ranking, information retrieval, tokenization",
     2020, "1st Edition", "AI-Floor-3-C6", 6, 3, 4.7, 230, "Production NLP, Text Processing"),

    ("Artificial Intelligence & Data Science", "Natural Language Processing", "Handbook", "Advanced",
     "Large Language Models: Architecture, Alignment, and Prompt Engineering", "Edward Beeching, Lewis Tunstall",
     "Comprehensive technical handbook on pre-training, fine-tuning (LoRA, QLoRA), instruction tuning, reinforcement learning from human feedback (RLHF), and evaluation of autoregressive transformer models.",
     "large language models, llm, transformers, rlhf, lora, fine-tuning, prompt engineering, nlp",
     2024, "1st Edition", "AI-Floor-3-C7", 6, 3, 4.9, 280, "LLM Architecture, Advanced NLP"),

    ("Artificial Intelligence & Data Science", "Computer Vision", "Lab Manual", "Beginner",
     "Computer Vision and Image Processing Lab Guide with OpenCV", "Gary Bradski, Adrian Kaehler",
     "Step-by-step laboratory experiments on digital image processing using OpenCV and Python. Covers color spaces, spatial filtering, edge detection (Canny, Sobel), image contours, and real-time object tracking.",
     "opencv, computer vision lab, image processing, edge detection, filtering, python opencv, lab manual",
     2021, "2nd Edition", "AI-Floor-3-B11", 8, 5, 4.6, 220, "OpenCV Lab, Image Processing"),

    ("Artificial Intelligence & Data Science", "Data Science & Analytics", "Textbook", "Beginner",
     "Python Data Science Handbook: Essential Tools for Working with Data", "Jake VanderPlas",
     "The definitive guide to core Python data science packages. Covers IPython, NumPy multi-dimensional arrays, Pandas data manipulation, Matplotlib/Seaborn visualization, and Scikit-Learn machine learning pipelines.",
     "python, data science, numpy, pandas, matplotlib, scikit-learn, data analysis, vanderplas",
     2023, "2nd Edition", "DS-Floor-3-A4", 9, 6, 4.9, 390, "VanderPlas, Python Data Science"),

    ("Artificial Intelligence & Data Science", "Data Science & Analytics", "Lab Manual", "Beginner",
     "Exploratory Data Analysis and Visualization Lab Workbook", "Wes McKinney, Hadley Wickham",
     "Interactive lab workbook focusing on dataset cleaning, missing value imputation, outlier detection, statistical hypothesis testing, and creating explanatory dashboards in Python.",
     "eda, data cleaning, pandas lab, visualization, exploratory data analysis, statistics, lab manual",
     2022, "Practical Lab Edition", "DS-Floor-3-A5", 8, 5, 4.7, 250, "EDA Lab, Data Cleaning"),

    ("Artificial Intelligence & Data Science", "Recommender Systems", "Reference Book", "Intermediate",
     "Practical Recommender Systems", "Kim Falk",
     "Comprehensive engineering guide to building industrial recommendation algorithms. Covers collaborative filtering, content-based recommendation using TF-IDF and item profiles, cold-start handling, and evaluation metrics.",
     "recommender systems, content-based filtering, tf-idf, collaborative filtering, cold start, precision, recall",
     2019, "1st Edition", "AI-Floor-3-C8", 5, 3, 4.8, 190, "Directly Relevant, Recommender Systems"),

    # --- Mathematics ---
    ("Mathematics", "Linear Algebra", "Textbook", "Intermediate",
     "Linear Algebra Done Right", "Sheldon Axler",
     "Renowned textbook that takes a coordinate-free approach focusing on linear operators on vector spaces rather than determinants. Covers invariant subspaces, inner-product spaces, spectral theorem, and singular value decomposition.",
     "linear algebra, vector spaces, axler, linear operators, eigenvalues, inner product, spectral theorem",
     2024, "4th Edition", "MA-Floor-1-A6", 8, 4, 4.9, 310, "Axler, Pure Linear Algebra"),

    ("Mathematics", "Linear Algebra", "Lab Manual", "Beginner",
     "Computational Linear Algebra with Python and NumPy", "Rachel Thomas, Jeremy Howard",
     "Practical computational laboratory course on implementing matrix factorization, QR decomposition, SVD, and principal component analysis from scratch using NumPy and Jupyter notebooks.",
     "linear algebra lab, numpy, python, matrix factorization, svd, pca, computational math, lab manual",
     2022, "Fast.ai Edition", "MA-Floor-1-A7", 7, 5, 4.8, 220, "Linear Algebra Lab, Python"),

    ("Mathematics", "Linear Algebra", "Handbook", "Advanced",
     "Matrix Computations", "Gene H. Golub, Charles F. Van Loan",
     "The definitive bible on numerical linear algebra algorithms. In-depth analysis of Gaussian elimination, Householder reflections, QR factorization, Lanczos algorithm, and Jacobi eigenvalue solvers.",
     "matrix computations, golub, van loan, numerical linear algebra, svd, qr decomposition, eigenvalues",
     2013, "4th Edition", "MA-Floor-1-A8", 5, 2, 4.9, 175, "Matrix Bible, Advanced"),

    ("Mathematics", "Calculus & Analysis", "Textbook", "Intermediate",
     "Advanced Engineering Mathematics", "Erwin Kreyszig",
     "Comprehensive standard textbook for engineering students. Detailed coverage of ordinary differential equations (ODEs), partial differential equations (PDEs), vector analysis, complex analysis, and Fourier transforms.",
     "engineering mathematics, kreyszig, differential equations, fourier transform, complex analysis, pde",
     2020, "10th Edition", "MA-Floor-1-C4", 10, 6, 4.8, 380, "Kreyszig, Engineering Math"),

    ("Mathematics", "Calculus & Analysis", "Lab Manual", "Beginner",
     "Engineering Calculus and Differential Equations Lab Manual", "James Stewart, Erwin Kreyszig",
     "Undergraduate laboratory workbook featuring computational problem solving using SymPy and MATLAB. Exercises on numerical integration, phase portraits of differential systems, and series approximations.",
     "calculus lab, differential equations, sympy, matlab, numerical integration, lab manual",
     2021, "Lab Edition", "MA-Floor-1-C5", 8, 5, 4.6, 205, "Calculus Lab, SymPy"),

    ("Mathematics", "Probability & Stochastic Processes", "Handbook", "Intermediate",
     "Probability and Statistics for Computer Scientists", "Michael Baron",
     "Applied statistics text tailored specifically for computer scientists. Covers Markov chains, Monte Carlo simulations, queuing theory, hypothesis testing, reliability modeling, and randomized algorithms.",
     "probability, statistics, computer science, markov chains, monte carlo, queuing theory, randomized algorithms",
     2019, "3rd Edition", "MA-Floor-1-B5", 7, 4, 4.7, 240, "CS Probability, Applied Statistics"),

    ("Mathematics", "Optimization", "Textbook", "Beginner",
     "Introduction to Applied Optimization", "Urmila Diwekar",
     "Accessible introduction to optimization modeling for engineering applications. Covers linear programming, simplex method, nonlinear optimization, genetic algorithms, and simulated annealing.",
     "optimization, linear programming, simplex, nonlinear optimization, genetic algorithms, diwekar",
     2020, "3rd Edition", "MA-Floor-1-D2", 6, 4, 4.6, 170, "Optimization Basics"),

    ("Mathematics", "Discrete Mathematics", "Lab Manual", "Beginner",
     "Discrete Mathematics and Graph Theory Lab Manual", "Kenneth H. Rosen",
     "Hands-on university lab workbook with algorithm implementation exercises in Python. Covers truth table generators, relation verification, tree traversals, topological sort, and bipartite graph matching.",
     "discrete math lab, graph theory, python, boolean logic, trees, relations, lab manual",
     2022, "University Lab Series", "MA-Floor-1-B6", 8, 6, 4.7, 210, "Discrete Math Lab"),

    # --- Cybersecurity & Networks ---
    ("Cybersecurity & Networks", "Cryptography", "Textbook", "Intermediate",
     "Understanding Cryptography: A Textbook for Students and Practitioners", "Christof Paar, Jan Pelzl",
     "Highly pedagogical introduction to modern cryptography. Explains stream ciphers, DES, AES, RSA, Diffie-Hellman key exchange, elliptic curve cryptography (ECC), and digital signature standards.",
     "cryptography, aes, rsa, ecc, elliptic curves, diffie-hellman, digital signatures, encryption, paar",
     2010, "1st Edition", "SEC-Floor-4-B3", 7, 4, 4.8, 280, "Modern Cryptography, Paar"),

    ("Cybersecurity & Networks", "Ethical Hacking & Systems Security", "Lab Manual", "Beginner",
     "Ethical Hacking and Penetration Testing Lab Manual", "Georgia Weidman",
     "Hands-on offensive security laboratory workbook. Exercises in setting up Kali Linux, network scanning with Nmap, vulnerability exploitation with Metasploit, password cracking with Hashcat, and privilege escalation.",
     "ethical hacking lab, penetration testing, nmap, metasploit, kali linux, exploits, lab manual",
     2022, "Lab Manual Edition", "SEC-Floor-4-C4", 8, 5, 4.8, 275, "Hacking Lab, Kali Linux"),

    ("Cybersecurity & Networks", "Web Application Security", "Lab Manual", "Intermediate",
     "Web Security Testing and OWASP Top 10 Lab Guide", "Dafydd Stuttard, Ryan C. Barnett",
     "Hands-on laboratory exercises using DVWA (Damn Vulnerable Web App) and Burp Suite. Step-by-step exploitation and remediation of SQL injection, cross-site scripting (XSS), CSRF, and broken access controls.",
     "web security lab, owasp top 10, sql injection, xss, burp suite, dvwa, penetration testing, lab manual",
     2021, "Practical Lab Series", "SEC-Floor-4-A4", 7, 4, 4.8, 230, "Web Security Lab, OWASP"),

    ("Cybersecurity & Networks", "Network Security", "Handbook", "Beginner",
     "Practical Packet Analysis: Using Wireshark to Solve Real-World Network Problems", "Chris Sanders",
     "Essential handbook on network troubleshooting and security traffic inspection. Covers packet crafting, TCP handshakes, identifying rogue DHCP servers, detecting port scans, and analyzing malware beaconing.",
     "wireshark, packet analysis, network security, packet capture, tcpdump, cybersecurity, troubleshooting",
     2017, "3rd Edition", "SEC-Floor-4-A5", 8, 5, 4.8, 290, "Wireshark Bible, Packet Analysis"),

    ("Cybersecurity & Networks", "Malware Analysis & Forensics", "Guide", "Intermediate",
     "Practical Cyber Forensics: An Incident-Based Approach", "Niranjan Reddy",
     "Comprehensive practitioner guide to digital evidence collection, hard drive imaging, memory forensics with Volatility, registry analysis, timeline reconstruction, and forensic report writing.",
     "digital forensics, cyber forensics, incident response, memory analysis, volatility, evidence, security",
     2019, "1st Edition", "SEC-Floor-4-B4", 6, 3, 4.6, 160, "Digital Forensics, Incident Response"),

    ("Cybersecurity & Networks", "Security Architecture & Modeling", "Reference Book", "Advanced",
     "Zero Trust Architecture: Protecting Enterprise Assets", "Jason Garbis, Jerry W. Chapman",
     "Architectural guide to implementing Zero Trust security. Explores identity-based perimeter security, micro-segmentation, continuous authentication, least-privilege access, and NIST SP 800-207 guidelines.",
     "zero trust, security architecture, network security, microsegmentation, identity management, enterprise",
     2021, "1st Edition", "SEC-Floor-4-D4", 5, 3, 4.7, 185, "Zero Trust Architecture"),

    # --- Electrical & Electronics Engineering ---
    ("Electrical & Electronics Engineering", "Electronic Circuits & Semiconductor Devices", "Lab Manual", "Beginner",
     "Electronic Devices and Circuits Laboratory Manual", "Adel S. Sedra, Kenneth C. Smith",
     "Fundamental undergraduate laboratory guide. Includes hands-on breadboard and oscilloscope experiments for diode characteristics, BJT amplifiers, MOSFET switching circuits, and op-amp filters.",
     "electronics lab, circuits lab, oscilloscope, bjt, mosfet, operational amplifiers, diodes, lab manual",
     2020, "8th Edition Companion", "EEE-Floor-1-A3", 9, 6, 4.7, 260, "Circuits Lab, Sedra Smith"),

    ("Electrical & Electronics Engineering", "Signal Processing", "Lab Manual", "Intermediate",
     "Digital Signal Processing Laboratory with MATLAB and Python", "Vinay K. Ingle, John G. Proakis",
     "Laboratory workbook containing coding exercises for discrete-time systems. Covers Fast Fourier Transform (FFT) verification, FIR filter design using windowing, IIR Butterworth filters, and audio noise filtering.",
     "dsp lab, matlab, python, fft, fir filters, iir filters, filter design, signal processing, lab manual",
     2021, "4th Edition Lab Series", "EEE-Floor-1-B2", 8, 5, 4.8, 240, "DSP Lab, MATLAB"),

    ("Electrical & Electronics Engineering", "Digital Logic & VLSI", "Lab Manual", "Beginner",
     "Digital Logic and FPGA Design Laboratory Workbook", "M. Morris Mano, Michael D. Ciletti",
     "Comprehensive lab workbook guiding students through logic gate synthesis, K-map minimization, combinational adder design, and Verilog HDL simulation on Xilinx FPGA development boards.",
     "fpga lab, digital logic lab, verilog, xilinx, logic gates, k-maps, combinational circuits, lab manual",
     2022, "FPGA Edition", "EEE-Floor-1-B3", 8, 5, 4.7, 210, "FPGA Lab, Verilog"),

    ("Electrical & Electronics Engineering", "Embedded Systems & IoT", "Handbook", "Intermediate",
     "Internet of Things: Principles and Paradigms", "Rajkumar Buyya, Amir Vahid Dastjerdi",
     "Comprehensive technical handbook on IoT architectures. Details sensor networks, RFID, MQTT protocol, CoAP, edge computing gateways, cloud analytics, and smart city implementations.",
     "iot, internet of things, mqtt, sensors, edge computing, smart systems, embedded, wireless sensors",
     2016, "1st Edition", "EEE-Floor-1-C4", 6, 3, 4.6, 215, "IoT Handbook, Edge Computing"),

    ("Electrical & Electronics Engineering", "Embedded Systems & IoT", "Lab Manual", "Beginner",
     "Arduino and ARM Embedded Systems Prototyping Lab Guide", "Jonathan W. Valvano, Massimo Banzi",
     "Hands-on lab manual for microcontroller hardware interfacing. Experiments with analog temperature sensors, PWM motor control, SPI displays, I2C real-time clocks, and UART serial communication.",
     "arduino, arm cortex, microcontrollers, embedded lab, sensors, pwm, uart, spi, i2c, lab manual",
     2021, "Prototyping Edition", "EEE-Floor-1-C5", 10, 7, 4.8, 310, "Embedded Lab, Arduino & ARM"),

    ("Electrical & Electronics Engineering", "Control Systems", "Lab Manual", "Intermediate",
     "Feedback Control Systems Simulation and Lab Workbook", "Norman S. Nise, Richard C. Dorf",
     "Laboratory guide using MATLAB and Simulink. Covers state-space modeling, root locus plotting, Bode frequency response verification, PID tuning for DC motor position control, and inverted pendulum stabilization.",
     "control systems lab, matlab, simulink, pid controller, bode plot, root locus, feedback, lab manual",
     2020, "Control Lab Series", "EEE-Floor-1-D4", 7, 4, 4.7, 190, "Control Lab, Simulink"),

    ("Electrical & Electronics Engineering", "Power Systems", "Handbook", "Advanced",
     "Renewable Energy Integration: Challenges and Solutions", "Jahangir Hossain, A. S. M. Mahmud",
     "State-of-the-art reference on integrating solar photovoltaic and wind energy into modern power grids. Covers inverter synchronization, microgrid stability, battery energy storage systems, and power quality.",
     "renewable energy, power systems, solar pv, wind turbines, microgrids, smart grid, inverter control",
     2020, "1st Edition", "EEE-Floor-1-E3", 5, 2, 4.7, 155, "Renewable Power, Smart Grid"),

    # --- Mechanical Engineering ---
    ("Mechanical Engineering", "Mechanics & Materials", "Lab Manual", "Beginner",
     "Strength of Materials and Material Testing Lab Manual", "Ferdinand P. Beer, Russell C. Hibbeler",
     "Undergraduate mechanical testing laboratory manual. Detailed experimental procedures for tensile testing on UTM, Charpy impact testing, Rockwell hardness measurement, torsion testing, and deflection of beams.",
     "material testing, utm, tensile test, hardness test, charpy impact, stress strain, lab manual",
     2020, "Standard Lab Series", "MEC-Floor-1-C4", 9, 6, 4.7, 280, "Strength of Materials Lab"),

    ("Mechanical Engineering", "Thermodynamics & Thermal Sciences", "Lab Manual", "Beginner",
     "Thermal Engineering and Heat Transfer Laboratory Manual", "Yunus A. Çengel, Frank P. Incropera",
     "Laboratory workbook for thermodynamics experiments. Includes trials on thermal conductivity measurement, forced and free convection heat transfer coefficients, heat exchanger performance, and refrigeration test rigs.",
     "thermal lab, heat transfer lab, heat exchanger, thermal conductivity, thermodynamics, lab manual",
     2021, "Thermal Engineering Edition", "MEC-Floor-1-A3", 8, 5, 4.8, 250, "Thermal Lab, Heat Exchanger"),

    ("Mechanical Engineering", "Robotics & Automation", "Guide", "Beginner",
     "Robot Operating System (ROS) for Absolute Beginners", "Lentin Joseph",
     "Practical beginner guide to robotics programming with ROS and Python. Covers nodes, topics, publishers, subscribers, ROS services, URDF robot modeling, Gazebo physics simulation, and autonomous navigation.",
     "ros, robot operating system, robotics, gazebo, navigation, python robotics, sensors, lidar",
     2018, "1st Edition", "MEC-Floor-1-B4", 7, 4, 4.7, 260, "ROS Guide, Robotics Software"),

    ("Mechanical Engineering", "Robotics & Automation", "Lab Manual", "Intermediate",
     "Robotics Kinematics and Motion Control Lab Manual", "John J. Craig, Mark W. Spong",
     "Laboratory guide focusing on mathematical modeling and simulation of robotic manipulators. Experiments on Denavit-Hartenberg parameters, inverse kinematics solvers, path planning, and obstacle avoidance in MATLAB.",
     "robotics lab, kinematics, inverse kinematics, dh parameters, trajectory planning, manipulators, lab manual",
     2022, "Robotics Lab Edition", "MEC-Floor-1-B5", 6, 4, 4.8, 195, "Robotics Lab, Kinematics"),

    ("Mechanical Engineering", "Computer-Aided Design & Manufacturing", "Handbook", "Intermediate",
     "Mastering SolidWorks: The Comprehensive Guide", "Matt Lombard",
     "Exhaustive industrial reference on parametric mechanical CAD. Details complex surface modeling, top-down assembly design, motion simulation, sheet metal fabrication design, and geometric dimensioning and tolerancing (GD&T).",
     "solidworks, cad, 3d modeling, mechanical design, assemblies, gd&t, parametric modeling, drafting",
     2021, "Updated Edition", "MEC-Floor-1-E3", 6, 3, 4.8, 240, "SolidWorks Handbook, CAD"),

    ("Mechanical Engineering", "Automotive & Energy Systems", "Textbook", "Beginner",
     "Automotive Engineering: Lightweight Materials and Vehicle Dynamics", "David Crolla",
     "Comprehensive introduction to vehicle powertrain design, suspension geometry, steering mechanisms, tire friction dynamics, crashworthiness simulation, and electric vehicle battery packaging.",
     "automotive engineering, vehicle dynamics, suspension, powertrain, electric vehicles, chassis design",
     2019, "2nd Edition", "MEC-Floor-1-D3", 7, 4, 4.6, 210, "Automotive Dynamics, EV"),

    # --- Biotechnology & Healthcare ---
    ("Biotechnology & Healthcare", "Bioinformatics & Genomics", "Lab Manual", "Beginner",
     "Bioinformatics Practical Laboratory Manual", "David W. Mount, Vince Buffalo",
     "Hands-on computational laboratory exercises in molecular biology. Step-by-step assignments using NCBI BLAST, EMBOSS sequence tools, Clustal Omega multiple sequence alignment, PyMOL 3D protein visualization, and Primer-BLAST.",
     "bioinformatics lab, blast, sequence alignment, pymol, ncbi, protein visualization, dna, lab manual",
     2022, "Lab Manual Edition", "BIO-Floor-4-A6", 8, 5, 4.7, 220, "Bioinformatics Lab, BLAST"),

    ("Biotechnology & Healthcare", "Biotechnology Fundamentals", "Lab Manual", "Beginner",
     "Molecular Biology and Genetic Engineering Laboratory Manual", "Bruce Alberts, James D. Watson",
     "Standard molecular biology wet-lab protocol manual. Includes protocols for bacterial plasmid DNA extraction, agarose gel electrophoresis, PCR amplification, restriction enzyme digestion, and bacterial transformation.",
     "molecular biology lab, pcr, gel electrophoresis, dna extraction, genetic engineering, cloning, lab manual",
     2021, "Laboratory Protocol Edition", "BIO-Floor-4-B4", 9, 6, 4.8, 270, "Wet Lab Manual, PCR & DNA"),

    ("Biotechnology & Healthcare", "AI in Healthcare & Biology", "Handbook", "Intermediate",
     "Deep Learning in Medical Image Analysis", "Kevin Zhou, Hayit Greenspan, Dinggang Shen",
     "Comprehensive technical handbook on applying convolutional networks and vision transformers to MRI, CT, and X-ray radiology scans. Covers image registration, organ segmentation, tumor detection, and FDA regulatory considerations.",
     "medical imaging, deep learning, radiology, ct scan, mri, image segmentation, healthcare ai, diagnosis",
     2020, "1st Edition", "BIO-Floor-4-A7", 5, 2, 4.8, 175, "Medical AI, Radiology Deep Learning"),

    ("Biotechnology & Healthcare", "Biotechnology Fundamentals", "Textbook", "Intermediate",
     "Principles of Fermentation Technology", "Peter F. Stanbury, Allan Whitaker, Stephen J. Hall",
     "Authoritative guide to industrial microbiology and microbial culture systems. Covers media formulation, sterilization kinetics, aerator design, batch and continuous fermentation, and bioreactor scale-up.",
     "fermentation, industrial microbiology, bioreactors, downstream processing, bioprocess, biotechnology",
     2016, "3rd Edition", "BIO-Floor-4-B5", 6, 3, 4.7, 160, "Fermentation Technology"),

    ("Biotechnology & Healthcare", "Bioinformatics & Genomics", "Reference Book", "Advanced",
     "Statistical Methods in Bioinformatics: An Introduction", "Warren J. Ewens, Gregory R. Grant",
     "Rigorous mathematical treatment of statistical algorithms in genomics. Details Hidden Markov Models (HMM) for gene finding, Poisson approximations in sequence matching, BLAST score statistics (E-values), and phylogenetic distance trees.",
     "bioinformatics statistics, hidden markov models, hmm, blast e-value, statistical genomics, phylogenetics",
     2005, "2nd Edition", "BIO-Floor-4-A8", 4, 1, 4.8, 130, "Genomics Math & Statistics"),

    # --- Management & Business Analytics ---
    ("Management & Business Analytics", "Business Analytics", "Lab Manual", "Beginner",
     "Business Analytics and Excel Modeling Lab Workbook", "James R. Evans, Wayne L. Winston",
     "Interactive laboratory workbook for decision modeling. Hands-on exercises with Excel Solver, Monte Carlo risk simulation, decision trees, linear programming for portfolio optimization, and regression forecasting.",
     "business analytics lab, excel solver, optimization, decision modeling, forecasting, regression, lab manual",
     2021, "Excel Modeling Edition", "MGT-Floor-3-A4", 9, 6, 4.7, 280, "Analytics Lab, Excel Solver"),

    ("Management & Business Analytics", "Business Analytics", "Handbook", "Intermediate",
     "Big Data Analytics: Methods and Applications", "Saamy Koubik, Vignesh Ramachandran",
     "Architectural and analytical handbook on enterprise big data pipelines. Covers Apache Spark SQL, data lakes, distributed machine learning with MLlib, customer churn modeling, and real-time dashboarding.",
     "big data, apache spark, business analytics, data lakes, mllib, customer analytics, business intelligence",
     2022, "1st Edition", "MGT-Floor-3-A5", 6, 3, 4.6, 210, "Big Data Analytics, Spark"),

    ("Management & Business Analytics", "Operations & Supply Chain", "Lab Manual", "Beginner",
     "Supply Chain Optimization and Operations Research Lab Manual", "Sunil Chopra, Frederick S. Hillier",
     "Practical laboratory manual featuring Python (SciPy/PuLP) and spreadsheet models for economic order quantity (EOQ), transportation problem formulation, warehouse location modeling, and queue analysis.",
     "supply chain lab, operations research, eoq, linear programming, logistics, inventory modeling, lab manual",
     2022, "Operations Lab Series", "MGT-Floor-3-B5", 8, 5, 4.6, 195, "Supply Chain Lab, PuLP"),

    ("Management & Business Analytics", "Product Management", "Handbook", "Intermediate",
     "Continuous Discovery Habits: Discover Products that Create Customer Value", "Teresa Torres",
     "Essential modern guide to product discovery. Explores opportunity solution trees, continuous customer interviewing, assumption testing, prototyping experiments, and aligning feature backlogs with business outcomes.",
     "product management, discovery, opportunity solution tree, agile, customer research, product strategy",
     2021, "1st Edition", "MGT-Floor-3-B6", 7, 4, 4.9, 290, "Product Discovery, Teresa Torres"),

    ("Management & Business Analytics", "Entrepreneurship & Innovation", "Textbook", "Intermediate",
     "Disciplined Entrepreneurship: 24 Steps to a Successful Startup", "Bill Aulet",
     "Structured MIT curriculum textbook for technological entrepreneurship. 24-step roadmap covering customer personas, total addressable market (TAM), core value proposition, pricing framework, and customer acquisition cost (CAC).",
     "entrepreneurship, mit, startup, business models, tam, value proposition, innovation, product market fit",
     2024, "Expanded Edition", "MGT-Floor-3-B7", 7, 4, 4.8, 275, "MIT Disciplined Entrepreneurship")
]

def generate_complete_catalog():
    catalog = load_base_catalog()
    current_count = len(catalog)
    print(f"Loaded {current_count} base canonical catalog items.")

    # Track domain counts
    domain_counts = {}
    for item in catalog:
        dom = item["subject"]
        domain_counts[dom] = domain_counts.get(dom, 0) + 1

    # First add the manually curated comprehensive entries
    for entry in ADDITIONAL_DOMAINS_DATA:
        current_count += 1
        dom_name = entry[0]
        prefix = dom_name[:3].upper()
        if dom_name == "Artificial Intelligence & Data Science":
            prefix = "AI"
        elif dom_name == "Computer Science":
            prefix = "CS"
        elif dom_name == "Mathematics":
            prefix = "MA"
        elif dom_name == "Cybersecurity & Networks":
            prefix = "SEC"
        elif dom_name == "Electrical & Electronics Engineering":
            prefix = "EEE"
        elif dom_name == "Mechanical Engineering":
            prefix = "MEC"
        elif dom_name == "Biotechnology & Healthcare":
            prefix = "BIO"
        elif dom_name == "Management & Business Analytics":
            prefix = "MGT"

        res_id = f"RES-{prefix}-{current_count:03d}"
        catalog.append({
            "resource_id": res_id,
            "title": entry[4],
            "authors": entry[5],
            "subject": dom_name,
            "topic": entry[1],
            "resource_type": entry[2],
            "difficulty_level": entry[3],
            "description": entry[6],
            "keywords": entry[7],
            "publication_year": entry[8],
            "edition": entry[9],
            "isbn": f"978-013{current_count:04d}1",
            "location_shelf": entry[10],
            "total_copies": entry[11],
            "available_copies": entry[12],
            "simulated_rating": entry[13],
            "simulated_borrow_count": entry[14],
            "tags": entry[15]
        })
        domain_counts[dom_name] = domain_counts.get(dom_name, 0) + 1

    # Further expand systematically until every single domain has at least 41 books (total 328+ items)
    all_domains = [
        "Computer Science",
        "Artificial Intelligence & Data Science",
        "Mathematics",
        "Cybersecurity & Networks",
        "Electrical & Electronics Engineering",
        "Mechanical Engineering",
        "Biotechnology & Healthcare",
        "Management & Business Analytics"
    ]

    target_per_domain = 41
    domain_subtopics = {
        "Computer Science": ["Algorithms & Data Structures", "Operating Systems", "Database Systems", "Computer Networks", "Distributed Systems", "Software Engineering"],
        "Artificial Intelligence & Data Science": ["Machine Learning", "Deep Learning", "Natural Language Processing", "Computer Vision", "Data Science & Analytics", "Recommender Systems"],
        "Mathematics": ["Linear Algebra", "Calculus & Analysis", "Probability & Stochastic Processes", "Optimization", "Discrete Mathematics", "Applied Mathematics"],
        "Cybersecurity & Networks": ["Cryptography", "Web Application Security", "Ethical Hacking & Systems Security", "Network Forensics", "Malware Analysis", "Security Architecture"],
        "Electrical & Electronics Engineering": ["Electronic Circuits & Semiconductor Devices", "Signal Processing", "Digital Logic & VLSI", "Embedded Systems & IoT", "Control Systems", "Power Systems"],
        "Mechanical Engineering": ["Mechanics & Materials", "Thermodynamics & Thermal Sciences", "Robotics & Automation", "Fluid Dynamics", "CAD & Manufacturing", "Automotive Systems"],
        "Biotechnology & Healthcare": ["Bioinformatics & Genomics", "Biotechnology Fundamentals", "AI in Healthcare & Biology", "Bioprocess Engineering", "Molecular Modeling"],
        "Management & Business Analytics": ["Business Analytics", "Operations & Supply Chain", "Product Management", "Entrepreneurship & Innovation", "Financial Analytics"]
    }

    diff_levels = ["Beginner", "Intermediate", "Advanced"]
    res_types = ["Textbook", "Reference Book", "Guide", "Handbook", "Lab Manual"]

    for dom in all_domains:
        current_in_dom = sum(1 for item in catalog if item["subject"] == dom)
        subtopics = domain_subtopics[dom]
        idx = 0
        while current_in_dom < target_per_domain:
            current_count += 1
            current_in_dom += 1
            topic = subtopics[idx % len(subtopics)]
            diff = diff_levels[idx % len(diff_levels)]
            rtype = res_types[idx % len(res_types)]

            prefix = dom[:3].upper()
            if dom == "Artificial Intelligence & Data Science":
                prefix = "AI"
            elif dom == "Computer Science":
                prefix = "CS"
            elif dom == "Mathematics":
                prefix = "MA"
            elif dom == "Cybersecurity & Networks":
                prefix = "SEC"
            elif dom == "Electrical & Electronics Engineering":
                prefix = "EEE"
            elif dom == "Mechanical Engineering":
                prefix = "MEC"
            elif dom == "Biotechnology & Healthcare":
                prefix = "BIO"
            elif dom == "Management & Business Analytics":
                prefix = "MGT"

            res_id = f"RES-{prefix}-{current_count:03d}"
            title = f"{topic}: Principles, Systems, and Practice (Vol. {current_in_dom})"
            authors = f"Academic Faculty Council, Dr. Research Scholar {current_count}"
            desc = (f"Comprehensive academic {rtype.lower()} dedicated to foundational and contemporary advances in {topic.lower()}. "
                    f"Provides rigorous mathematical formulations, pedagogical curriculum case studies, verified homework problems, "
                    f"and applied laboratory demonstrations tailored for university degree programs at the {diff.lower()} level.")
            keywords = f"{topic.lower()}, {dom.lower()}, curriculum foundations, theoretical analysis, hands-on engineering, problem solving"
            year = 2018 + (idx % 7)
            edition = f"{1 + (idx % 4)}th Edition"
            shelf = f"{prefix}-Floor-{1 + (idx % 4)}-Rack-{chr(65 + (idx % 8))}"
            total_copies = 5 + (idx % 6)
            # Ensure 85% have copies > 0, 15% checked out
            avail_copies = 0 if (idx % 7 == 0) else (2 + (idx % 5))
            rating = round(4.3 + (idx % 7) * 0.1, 1)
            borrows = 90 + (idx * 17) % 320

            catalog.append({
                "resource_id": res_id,
                "title": title,
                "authors": authors,
                "subject": dom,
                "topic": topic,
                "resource_type": rtype,
                "difficulty_level": diff,
                "description": desc,
                "keywords": keywords,
                "publication_year": year,
                "edition": edition,
                "isbn": f"978-013{current_count:04d}X",
                "location_shelf": shelf,
                "total_copies": total_copies,
                "available_copies": avail_copies,
                "simulated_rating": rating,
                "simulated_borrow_count": borrows,
                "tags": f"Curriculum Essential, {dom}, University Accredited"
            })
            idx += 1

    return catalog

def main():
    os.makedirs("data", exist_ok=True)
    catalog = generate_complete_catalog()
    print(f"Total catalog entries generated: {len(catalog)}")
    
    # Check counts per domain
    domain_counts = {}
    for item in catalog:
        d = item["subject"]
        domain_counts[d] = domain_counts.get(d, 0) + 1
    for d, c in domain_counts.items():
        print(f"  • {d}: {c} books")

    fieldnames = [
        "resource_id", "title", "authors", "subject", "topic",
        "resource_type", "difficulty_level", "description", "keywords",
        "publication_year", "edition", "isbn", "location_shelf",
        "total_copies", "available_copies", "simulated_rating",
        "simulated_borrow_count", "tags"
    ]
    
    csv_path = os.path.join("data", "library_resources.csv")
    with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in catalog:
            writer.writerow(row)
            
    print(f"Successfully wrote {len(catalog)} resources to {csv_path}")

if __name__ == "__main__":
    main()
