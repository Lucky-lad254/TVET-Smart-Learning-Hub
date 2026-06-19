#!/usr/bin/env python
"""Application entry point."""

import os
from app import create_app, db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    print("\n" + "="*60)
    print("TVET Smart Learning Hub - Phase 1")
    print("="*60)
    print(f"\n🚀 Starting application...")
    print(f"📍 Access at: http://localhost:{port}")
    print(f"\n✅ Demo Accounts:")
    print(f"   Admin:   admin@tvet.edu / admin123")
    print(f"   Teacher: teacher@tvet.edu / teacher123")
    print(f"   Student: student@tvet.edu / student123")
    print(f"\n⚠️  Change default passwords in production!")
    print("\n" + "="*60 + "\n")
    
    app.run(host='0.0.0.0', port=port, debug=debug)
