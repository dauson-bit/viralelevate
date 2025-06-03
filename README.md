# ViralElevate

A comprehensive social media management and growth platform built with Django.

## Features

- Social Media Management
- One-Time Growth Services
- Package Services
- Payment Integration (M-PESA, Tigo Pesa, Airtel Money, HaloPesa)
- User Dashboard
- Order Management

## Technologies Used

- Python/Django
- HTML/CSS/JavaScript
- Bootstrap
- Mobile Money APIs

## Installation

1. Clone the repository:
```bash
git clone https://github.com/dauson-bit/viralelevate.git
cd viralelevate
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Start the development server:
```bash
python manage.py runserver
```

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```
DEBUG=True
SECRET_KEY=your_secret_key
DATABASE_URL=your_database_url
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 