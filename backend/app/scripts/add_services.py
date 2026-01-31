"""
Script to add service categories and services to the database.
Run with: uv run python -m app.scripts.add_services
For CI/non-interactive: uv run python -m app.scripts.add_services --yes
"""

import argparse
import uuid

from sqlmodel import Session, select

from app.core.db import engine
from app.models import Category, Service

# Define all categories and their services
SERVICES_DATA = {
    "Graphics & Design": [
        "Web Design",
        "UX/UI Design",
        "Logo Design",
        "Graphic Design",
        "Print Design",
        "3D Modeling",
        "Motion Graphics",
        "Illustration",
        "Branding",
        "Icon Design",
    ],
    "IT Consulting": [
        "IT Strategy",
        "Cloud Consulting",
        "Cybersecurity Consulting",
        "DevOps Consulting",
        "E-commerce Consulting",
        "AR/VR Consulting",
        "AI Consulting",
        "QA Consulting",
    ],
    "Application Development": [
        "Mobile App Development",
        "Web App Development",
        "Backend & API Development",
        "Frontend Development",
        "Fullstack Development",
    ],
    "Artificial Intelligence": [
        "AI Development",
        "Generative AI",
        "AI Agents",
        "Machine Learning",
        "Computer Vision",
    ],
    "Digital Marketing": [
        "Social Media Marketing",
        "PPC Advertising",
        "SEO Services",
        "Content Marketing",
        "Email Marketing",
    ],
    "Cloud Services": [
        "Cloud Migration",
        "Cloud Infrastructure",
        "Cloud Security",
        "Cloud Storage",
        "Serverless Architecture",
    ],
    "Data Science & Analytics": [
        "Business Intelligence",
        "Big Data Solutions",
        "Data Visualization",
        "Predictive Analytics",
        "Data Mining",
    ],
    "Cybersecurity Services": [
        "Security Audits",
        "Penetration Testing",
        "Incident Response",
        "Network Security",
        "Application Security",
    ],
    "Quality Assurance": [
        "Manual Testing",
        "Automated Testing",
        "Performance Testing",
        "Security Testing",
    ],
    "Blockchain Development": [
        "Smart Contracts",
        "DApp Development",
        "NFT Solutions",
        "Blockchain Consulting",
        "DeFi Development",
    ],
    "E-commerce Solutions": [
        "Online Store Development",
        "Marketplace Platforms",
        "Payment Integration",
        "Shopping Cart Solutions",
    ],
    "IT Support & Maintenance": [
        "Technical Support",
        "System Administration",
        "Server Maintenance",
        "Database Administration",
        "IT Monitoring",
    ],
    "Content Creation": [
        "Copywriting",
        "Technical Writing",
        "Video Production",
        "Photography",
        "Content Strategy",
    ],
    "Marketing Analytics": [
        "Web Analytics",
        "Social Media Analytics",
        "Conversion Optimization",
        "Marketing Dashboards",
        "ROI Analysis",
    ],
    "Software Integration": [
        "API Integration",
        "Third-party Integrations",
        "Legacy System Integration",
        "Middleware Development",
        "Data Migration",
    ],
    "AR/VR Development": [
        "Augmented Reality Apps",
        "Virtual Reality Solutions",
        "3D Simulation",
        "Mixed Reality",
    ],
    "IoT Development": [
        "Connected Devices",
        "IoT Platforms",
        "Sensor Integration",
        "IoT Analytics",
        "Industrial IoT",
    ],
    "Game Development": [
        "Mobile Games",
        "PC Games",
        "Game Design",
        "Game Porting",
        "Game Testing",
    ],
    "CRM/ERP Solutions": [
        "CRM Implementation",
        "ERP Systems",
        "Sales Automation",
        "Inventory Management",
        "Business Process Automation",
    ],
}


def add_services(*, yes: bool = False) -> None:
    """Add all service categories and services to the database."""
    with Session(engine) as session:
        # Check if we already have categories
        existing_categories = session.exec(select(Category)).first()
        if existing_categories and not yes:
            print("⚠️  Categories already exist in the database.")  # noqa: T201
            response = input("Do you want to add services anyway? (y/N): ")
            if response.lower() != "y":
                print("Aborted.")  # noqa: T201
                return

        total_categories = 0
        total_services = 0

        for category_name, services in SERVICES_DATA.items():
            print(f"\n📁 Processing category: {category_name}")  # noqa: T201

            # Check if category exists
            category = session.exec(
                select(Category).where(Category.label == category_name)
            ).first()

            if not category:
                # Create new category
                category = Category(
                    id=uuid.uuid4(),
                    label=category_name,
                )
                session.add(category)
                session.flush()  # Flush to get the ID
                total_categories += 1
                print(f"  ✅ Created category: {category_name}")  # noqa: T201
            else:
                print(f"  ℹ️  Category already exists: {category_name}")  # noqa: T201

            # Add services to this category
            for service_name in services:
                # Check if service exists
                existing_service = session.exec(
                    select(Service).where(Service.label == service_name)
                ).first()

                if not existing_service:
                    service = Service(
                        id=uuid.uuid4(),
                        label=service_name,
                        category_id=category.id,
                    )
                    session.add(service)
                    total_services += 1
                    print(f"    ✅ Added service: {service_name}")  # noqa: T201
                else:
                    print(f"    ℹ️  Service already exists: {service_name}")  # noqa: T201

        # Commit all changes
        session.commit()

        print("\n" + "=" * 60)  # noqa: T201
        print("✨ Successfully added:")  # noqa: T201
        print(f"   📁 Categories: {total_categories}")  # noqa: T201
        print(f"   🔧 Services: {total_services}")  # noqa: T201
        print("=" * 60)  # noqa: T201


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Add service categories and services to the database.")
    parser.add_argument(
        "--yes",
        "-y",
        action="store_true",
        help="Non-interactive mode: always add missing data, skip confirmation prompt (for CI)",
    )
    args = parser.parse_args()

    print("🚀 Adding service categories and services to the database...")  # noqa: T201
    print("=" * 60)  # noqa: T201
    add_services(yes=args.yes)


if __name__ == "__main__":
    main()
