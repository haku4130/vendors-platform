"""
Seed script for local development database.
Run inside the backend container:
  docker exec vendors-platform-backend-1 python scripts/seed.py
"""

import uuid

from sqlmodel import Session

from app.core.db import engine
from app.core.security import get_password_hash
from app.m2m_models import ProjectServiceLink, ProjectShortlist, VendorServiceLink
from app.models import (
    Category,
    Project,
    ProjectRequest,
    ProjectStart,
    RequestInitiator,
    RequestStatus,
    Review,
    Service,
    User,
    UserRole,
    VendorProfile,
)

PASSWORD_HASH = get_password_hash("Password123!")

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

CATEGORIES_WITH_SERVICES = {
    "Разработка": [
        "Веб-разработка",
        "Мобильная разработка",
        "Разработка ПО на заказ",
        "Разработка API и интеграции",
        "Разработка на 1С",
        "DevOps и CI/CD",
        "Разработка микросервисов",
    ],
    "Дизайн": [
        "UI/UX дизайн",
        "Брендинг и айдентика",
        "Продуктовый дизайн",
        "Дизайн мобильных приложений",
    ],
    "Данные и аналитика": [
        "Data Engineering",
        "BI и аналитика",
        "Машинное обучение и AI",
        "Data Science",
        "Визуализация данных",
    ],
    "Инфраструктура": [
        "Облачные решения (AWS/GCP/Azure)",
        "Администрирование серверов",
        "Кибербезопасность",
        "Сетевая инфраструктура",
    ],
    "Маркетинг и продвижение": [
        "SEO-продвижение",
        "Контекстная реклама",
        "SMM",
        "Email-маркетинг",
        "Контент-маркетинг",
    ],
    "Тестирование": [
        "QA и ручное тестирование",
        "Автотестирование",
        "Нагрузочное тестирование",
    ],
    "Консалтинг": [
        "IT-консалтинг",
        "Цифровая трансформация",
        "Архитектура систем",
        "Управление проектами",
    ],
}

VENDORS = [
    {
        "email": "info@techcraft.ru",
        "full_name": "Алексей Воронов",
        "company_name": "TechCraft Solutions",
        "location": "Москва",
        "main_goal": "Разрабатываем высоконагруженные веб-платформы и микросервисные архитектуры для крупного бизнеса.",
        "sales_email": "sales@techcraft.ru",
        "admin_contact_phone": "+7 495 123-45-67",
        "employee_count": 85,
        "company_website": "https://techcraft.ru",
        "founded_year": 2015,
        "turnover": 180_000_000,
        "description": "TechCraft Solutions — технологическая компания с фокусом на enterprise-разработку. Реализовали более 200 проектов для банков, ритейла и телекома. Стек: Python, Go, React, Kubernetes.",
        "min_project_size": 500_000,
        "avg_hourly_rate": 4500,
        "service_keys": [
            "Веб-разработка",
            "Разработка API и интеграции",
            "DevOps и CI/CD",
            "Разработка микросервисов",
            "Архитектура систем",
        ],
    },
    {
        "email": "hello@pixelstudio.ru",
        "full_name": "Мария Козлова",
        "company_name": "Pixel Studio",
        "location": "Санкт-Петербург",
        "main_goal": "Создаём продуктовый дизайн и интерфейсы, которые влюбляют пользователей в продукт с первого экрана.",
        "sales_email": "work@pixelstudio.ru",
        "admin_contact_phone": "+7 812 987-65-43",
        "employee_count": 28,
        "company_website": "https://pixelstudio.ru",
        "founded_year": 2018,
        "turnover": 45_000_000,
        "description": "Дизайн-студия с портфолио более 150 цифровых продуктов. Специализируемся на SaaS, финтехе и e-commerce. Победители Red Dot 2023.",
        "min_project_size": 150_000,
        "avg_hourly_rate": 3200,
        "service_keys": [
            "UI/UX дизайн",
            "Продуктовый дизайн",
            "Дизайн мобильных приложений",
            "Брендинг и айдентика",
            "Веб-разработка",
        ],
    },
    {
        "email": "team@datastream.io",
        "full_name": "Дмитрий Новиков",
        "company_name": "DataStream Analytics",
        "location": "Москва",
        "main_goal": "Превращаем сырые данные компании в инсайты, которые увеличивают выручку и снижают издержки.",
        "sales_email": "bd@datastream.io",
        "admin_contact_phone": "+7 495 234-56-78",
        "employee_count": 42,
        "company_website": "https://datastream.io",
        "founded_year": 2017,
        "turnover": 95_000_000,
        "description": "Специализируемся на построении data-платформ, ML-моделей и аналитических дашбордов. Клиенты: Сбер, X5, Магнит. Apache Spark, Airflow, Python, Tableau.",
        "min_project_size": 300_000,
        "avg_hourly_rate": 5000,
        "service_keys": [
            "Data Engineering",
            "BI и аналитика",
            "Машинное обучение и AI",
            "Data Science",
            "Визуализация данных",
        ],
    },
    {
        "email": "contact@mobilefirst.ru",
        "full_name": "Екатерина Смирнова",
        "company_name": "MobileFirst Dev",
        "location": "Казань",
        "main_goal": "Разрабатываем нативные и кросс-платформенные мобильные приложения с рейтингом 4.8+ в сторах.",
        "sales_email": "sales@mobilefirst.ru",
        "admin_contact_phone": "+7 843 345-67-89",
        "employee_count": 35,
        "company_website": "https://mobilefirst.ru",
        "founded_year": 2016,
        "turnover": 72_000_000,
        "description": "Топ-10 студий мобильной разработки по версии Ruward. Наши приложения суммарно скачали более 5 млн раз. iOS (Swift), Android (Kotlin), Flutter, React Native.",
        "min_project_size": 400_000,
        "avg_hourly_rate": 3800,
        "service_keys": [
            "Мобильная разработка",
            "UI/UX дизайн",
            "Разработка API и интеграции",
            "QA и ручное тестирование",
            "Автотестирование",
        ],
    },
    {
        "email": "info@cloudops.tech",
        "full_name": "Игорь Петров",
        "company_name": "CloudOps Technology",
        "location": "Новосибирск",
        "main_goal": "Строим отказоустойчивую облачную инфраструктуру и обеспечиваем безопасность данных бизнеса.",
        "sales_email": "sales@cloudops.tech",
        "admin_contact_phone": "+7 383 456-78-90",
        "employee_count": 55,
        "company_website": "https://cloudops.tech",
        "founded_year": 2014,
        "turnover": 130_000_000,
        "description": "Сертифицированный AWS Premier Partner и Google Cloud Partner. Помогаем мигрировать в облако, оптимизировать затраты и выстраивать DevSecOps практики.",
        "min_project_size": 200_000,
        "avg_hourly_rate": 4200,
        "service_keys": [
            "Облачные решения (AWS/GCP/Azure)",
            "DevOps и CI/CD",
            "Кибербезопасность",
            "Администрирование серверов",
            "Архитектура систем",
        ],
    },
    {
        "email": "hi@growthlab.ru",
        "full_name": "Анна Федорова",
        "company_name": "GrowthLab Digital",
        "location": "Москва",
        "main_goal": "Системно увеличиваем онлайн-продажи через комплексный digital-маркетинг с измеримым ROI.",
        "sales_email": "agency@growthlab.ru",
        "admin_contact_phone": "+7 495 567-89-01",
        "employee_count": 60,
        "company_website": "https://growthlab.ru",
        "founded_year": 2019,
        "turnover": 85_000_000,
        "description": "Performance-агентство с фокусом на e-commerce и SaaS. Управляем бюджетами более 500 млн рублей в год. Кейсы роста от 40% до 300% за 6 месяцев.",
        "min_project_size": 100_000,
        "avg_hourly_rate": 2800,
        "service_keys": [
            "SEO-продвижение",
            "Контекстная реклама",
            "SMM",
            "Email-маркетинг",
            "Контент-маркетинг",
        ],
    },
    {
        "email": "dev@softline.company",
        "full_name": "Сергей Кузнецов",
        "company_name": "Softline Company",
        "location": "Екатеринбург",
        "main_goal": "Автоматизируем бизнес-процессы на платформе 1С и создаём интеграции с любыми корпоративными системами.",
        "sales_email": "1c@softline.company",
        "admin_contact_phone": "+7 343 678-90-12",
        "employee_count": 120,
        "company_website": "https://softline.company",
        "founded_year": 2010,
        "turnover": 250_000_000,
        "description": "Один из крупнейших 1С-партнёров в Уральском регионе. Золотой статус 1С. Автоматизировали более 500 предприятий: производство, торговля, логистика.",
        "min_project_size": 80_000,
        "avg_hourly_rate": 2500,
        "service_keys": [
            "Разработка на 1С",
            "Разработка API и интеграции",
            "IT-консалтинг",
            "Цифровая трансформация",
            "Управление проектами",
        ],
    },
    {
        "email": "hello@qualitylab.dev",
        "full_name": "Наталья Орлова",
        "company_name": "QualityLab",
        "location": "Санкт-Петербург",
        "main_goal": "Находим баги до пользователей. Комплексное тестирование любой сложности в agile-командах.",
        "sales_email": "projects@qualitylab.dev",
        "admin_contact_phone": "+7 812 789-01-23",
        "employee_count": 45,
        "company_website": "https://qualitylab.dev",
        "founded_year": 2020,
        "turnover": 38_000_000,
        "description": "Независимая QA-лаборатория. Функциональное, регрессионное, нагрузочное и автоматизированное тестирование. Selenium, Cypress, JMeter, Playwright.",
        "min_project_size": 120_000,
        "avg_hourly_rate": 2900,
        "service_keys": [
            "QA и ручное тестирование",
            "Автотестирование",
            "Нагрузочное тестирование",
            "Веб-разработка",
            "Разработка API и интеграции",
        ],
    },
]

COMPANIES = [
    {
        "email": "tech@retailmax.ru",
        "full_name": "Владимир Захаров",
        "company_name": "RetailMax",
        "location": "Москва",
    },
    {
        "email": "it@finbridge.ru",
        "full_name": "Ольга Морозова",
        "company_name": "FinBridge",
        "location": "Санкт-Петербург",
    },
    {
        "email": "cto@logisticore.ru",
        "full_name": "Павел Соколов",
        "company_name": "LogistiCore",
        "location": "Казань",
    },
    {
        "email": "digital@medplus.ru",
        "full_name": "Инна Белова",
        "company_name": "MedPlus",
        "location": "Москва",
    },
    {
        "email": "it@agrotech.ru",
        "full_name": "Роман Николаев",
        "company_name": "AgroTech",
        "location": "Краснодар",
    },
]

PROJECTS = [
    {
        "title": "Редизайн личного кабинета клиента",
        "description": "Полный редизайн личного кабинета для 200 тыс. активных пользователей. Текущий интерфейс устарел, нужен современный UX с адаптивной вёрсткой. Интеграция с мобильным приложением.",
        "start_date": ProjectStart.within_30_days,
        "location": "Москва (возможно удалённо)",
        "website": "https://retailmax.ru",
        "budget": 1_500_000,
        "service_keys": ["UI/UX дизайн", "Веб-разработка"],
        "company_idx": 0,
    },
    {
        "title": "Разработка системы аналитики транзакций",
        "description": "Нужна real-time аналитика по банковским транзакциям с ML-моделями для выявления мошенничества. Объём: ~50 млн транзакций в сутки. Интеграция с Core Banking.",
        "start_date": ProjectStart.within_60_days,
        "location": "Санкт-Петербург",
        "website": "https://finbridge.ru",
        "budget": 5_000_000,
        "service_keys": [
            "Data Engineering",
            "Машинное обучение и AI",
            "Разработка API и интеграции",
        ],
        "company_idx": 1,
    },
    {
        "title": "Мобильное приложение для курьеров",
        "description": "iOS + Android приложение для курьеров с оффлайн-режимом, сканированием штрих-кодов, GPS-трекингом и push-уведомлениями. Интеграция с WMS и CRM системами.",
        "start_date": ProjectStart.within_30_days,
        "location": "Казань (удалённо)",
        "website": "https://logisticore.ru",
        "budget": 2_800_000,
        "service_keys": ["Мобильная разработка", "Разработка API и интеграции"],
        "company_idx": 2,
    },
    {
        "title": "Платформа телемедицины",
        "description": "Веб-платформа для онлайн-консультаций врачей с видеосвязью, электронными рецептами и историей болезни. Соответствие 152-ФЗ и медицинским регуляторным требованиям.",
        "start_date": ProjectStart.within_60_days,
        "location": "Москва",
        "website": "https://medplus.ru",
        "budget": 8_000_000,
        "service_keys": ["Разработка ПО на заказ", "UI/UX дизайн", "Кибербезопасность"],
        "company_idx": 3,
    },
    {
        "title": "Автоматизация учёта сельхозтехники на 1С",
        "description": "Внедрение 1С:ERP для учёта парка техники (200+ единиц), планирования ТО, расхода топлива и запчастей. Интеграция с датчиками ГЛОНАСС.",
        "start_date": ProjectStart.after_60_days,
        "location": "Краснодар",
        "website": "https://agrotech.ru",
        "budget": 1_200_000,
        "service_keys": ["Разработка на 1С", "IT-консалтинг"],
        "company_idx": 4,
    },
    {
        "title": "SEO и performance-маркетинг для e-commerce",
        "description": "Комплексное продвижение интернет-магазина: SEO-аудит и оптимизация, настройка контекстной рекламы в Яндексе, ретаргетинг. KPI: рост органического трафика на 50% за 6 мес.",
        "start_date": ProjectStart.within_30_days,
        "location": "Москва (удалённо)",
        "website": "https://retailmax.ru",
        "budget": 600_000,
        "service_keys": ["SEO-продвижение", "Контекстная реклама"],
        "company_idx": 0,
    },
    {
        "title": "Миграция инфраструктуры в Яндекс.Облако",
        "description": "Перенос 40+ микросервисов из on-premise в YandexCloud. Настройка Kubernetes-кластеров, CI/CD пайплайнов, мониторинга и алертинга. SLA 99.95%.",
        "start_date": ProjectStart.within_60_days,
        "location": "Санкт-Петербург (удалённо)",
        "website": "https://finbridge.ru",
        "budget": 3_500_000,
        "service_keys": ["Облачные решения (AWS/GCP/Azure)", "DevOps и CI/CD"],
        "company_idx": 1,
    },
    {
        "title": "Нагрузочное тестирование платёжного сервиса",
        "description": "Проведение нагрузочного и стресс-тестирования платёжного API перед запуском маркетплейса. Целевая нагрузка: 10 000 RPS. Нужен отчёт с рекомендациями по оптимизации.",
        "start_date": ProjectStart.within_30_days,
        "location": "Удалённо",
        "website": "https://logisticore.ru",
        "budget": 350_000,
        "service_keys": ["Нагрузочное тестирование", "QA и ручное тестирование"],
        "company_idx": 2,
    },
]

REVIEWS_DATA = [
    {
        "rating": 5,
        "comment": "Команда TechCraft полностью оправдала ожидания. Сдали проект в срок, код чистый, документация подробная. Однозначно рекомендуем.",
    },
    {
        "rating": 4,
        "comment": "Хорошая работа, дизайн получился современным. Были небольшие задержки на этапе согласований, но в целом довольны результатом.",
    },
    {
        "rating": 5,
        "comment": "DataStream — настоящие профессионалы в аналитике. Построили data-платформу, которая обрабатывает 10 млрд событий в день. Сотрудничаем уже 2 года.",
    },
    {
        "rating": 4,
        "comment": "Мобильное приложение запустили вовремя. Команда профессиональная, на вопросы отвечают быстро. Небольшие правки пришлось вносить после релиза.",
    },
    {
        "rating": 5,
        "comment": "CloudOps грамотно спроектировали инфраструктуру. После миграции в облако сократили затраты на 30%. Поддержка работает оперативно.",
    },
]


# ---------------------------------------------------------------------------
# Seeding functions
# ---------------------------------------------------------------------------


def seed(session: Session) -> None:
    print("🌱 Starting seed...")

    # Categories & Services
    print("  → Categories & Services")
    service_map: dict[str, uuid.UUID] = {}
    for cat_label, service_labels in CATEGORIES_WITH_SERVICES.items():
        cat = Category(label=cat_label)
        session.add(cat)
        session.flush()
        for svc_label in service_labels:
            svc = Service(label=svc_label, category_id=cat.id)
            session.add(svc)
            session.flush()
            service_map[svc_label] = svc.id
    session.commit()
    print(
        f"     {len(service_map)} services across {len(CATEGORIES_WITH_SERVICES)} categories"
    )

    # Vendor users + profiles
    print("  → Vendor users & profiles")
    vendor_profiles: list[VendorProfile] = []
    for v in VENDORS:
        user = User(
            email=v["email"],
            full_name=v["full_name"],
            company_name=v["company_name"],
            location=v["location"],
            role=UserRole.vendor,
            hashed_password=PASSWORD_HASH,
        )
        session.add(user)
        session.flush()

        profile = VendorProfile(
            user_id=user.id,
            main_goal=v["main_goal"],
            sales_email=v["sales_email"],
            admin_contact_phone=v["admin_contact_phone"],
            employee_count=v["employee_count"],
            company_website=v["company_website"],
            founded_year=v["founded_year"],
            turnover=v["turnover"],
            description=v["description"],
            min_project_size=v["min_project_size"],
            avg_hourly_rate=v["avg_hourly_rate"],
        )
        session.add(profile)
        session.commit()

        for svc_key in v["service_keys"]:
            link = VendorServiceLink(
                vendor_profile_id=profile.id, service_id=service_map[svc_key]
            )
            session.add(link)
        session.commit()

        vendor_profiles.append(profile)
    print(f"     {len(vendor_profiles)} vendors created")

    # Company users
    print("  → Company users")
    company_users: list[User] = []
    for c in COMPANIES:
        user = User(
            email=c["email"],
            full_name=c["full_name"],
            company_name=c["company_name"],
            location=c["location"],
            role=UserRole.company,
            hashed_password=PASSWORD_HASH,
        )
        session.add(user)
        session.flush()
        company_users.append(user)
    session.commit()
    print(f"     {len(company_users)} companies created")

    # Projects
    print("  → Projects")
    projects: list[Project] = []
    for p in PROJECTS:
        owner = company_users[p["company_idx"]]
        project = Project(
            title=p["title"],
            description=p["description"],
            start_date=p["start_date"],
            location=p["location"],
            website=p["website"],
            budget=p["budget"],
            owner_id=owner.id,
        )
        session.add(project)
        session.commit()
        for svc_key in p["service_keys"]:
            link = ProjectServiceLink(
                project_id=project.id, service_id=service_map[svc_key]
            )
            session.add(link)
        session.commit()
        projects.append(project)
    print(f"     {len(projects)} projects created")

    # Project requests (vendors → projects)
    print("  → Project requests")
    requests_created = 0
    pairs = [
        (0, 0),
        (1, 0),
        (2, 0),  # project 0: 3 vendors applied
        (2, 1),
        (3, 1),  # project 1: 2 vendors
        (3, 2),
        (7, 2),  # project 2
        (1, 3),
        (0, 3),
        (4, 3),  # project 3: 3 vendors
        (6, 4),  # project 4
        (5, 5),  # project 5
        (4, 6),  # project 6
        (7, 7),  # project 7
    ]
    statuses = [
        RequestStatus.sent,
        RequestStatus.accepted,
        RequestStatus.sent,
        RequestStatus.declined,
    ]
    for i, (vendor_idx, project_idx) in enumerate(pairs):
        req = ProjectRequest(
            vendor_profile_id=vendor_profiles[vendor_idx].id,
            project_id=projects[project_idx].id,
            initiator=RequestInitiator.vendor,
            status=statuses[i % len(statuses)],
        )
        session.add(req)
        requests_created += 1
    session.commit()
    print(f"     {requests_created} requests created")

    # Shortlists (projects ↔ vendor profiles)
    print("  → Shortlists")
    shortlist_pairs = [(0, 0), (0, 1), (0, 2), (1, 2), (1, 3), (2, 0), (3, 4), (3, 5)]
    for project_idx, vendor_idx in shortlist_pairs:
        sl = ProjectShortlist(
            project_id=projects[project_idx].id,
            vendor_profile_id=vendor_profiles[vendor_idx].id,
        )
        session.add(sl)
    session.commit()
    print(f"     {len(shortlist_pairs)} shortlist entries")

    # Reviews
    print("  → Reviews")
    for i, rv in enumerate(REVIEWS_DATA):
        author = company_users[i % len(company_users)]
        reviewed_user_id = vendor_profiles[i % len(vendor_profiles)].user_id
        review = Review(
            author_id=author.id,
            reviewed_user_id=reviewed_user_id,
            rating=rv["rating"],
            text=rv["comment"],
            project_id=projects[i].id,
        )
        session.add(review)
    session.commit()
    print(f"     {len(REVIEWS_DATA)} reviews created")

    print("\n✅ Seed complete!")
    print("   All vendor/company passwords: Password123!")


if __name__ == "__main__":
    # Check Review model fields first
    with Session(engine) as session:
        # Quick check existing data
        from sqlmodel import select as sel

        existing = session.exec(sel(User).where(User.role == UserRole.vendor)).all()
        if existing:
            print(
                f"⚠️  Database already has {len(existing)} vendor users. Skipping seed."
            )
            print("   To re-seed, clear the database first.")
        else:
            seed(session)
