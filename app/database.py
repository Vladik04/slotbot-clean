"""SQLite база данных для бота."""

import sqlite3
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)


class Database:
    """Управление SQLite базой данных."""
    
    def __init__(self, db_path: str = "app/data/bot.db"):
        """Инициализировать БД."""
        self.db_path = db_path
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self.init_db()
    
    def get_connection(self) -> sqlite3.Connection:
        """Получить подключение к БД."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self) -> None:
        """Инициализировать таблицы БД."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Таблица пользователей
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    is_vip INTEGER DEFAULT 0,
                    vip_expires_at TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Таблица событий
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    event_type TEXT NOT NULL,
                    data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            """)
            
            # Таблица платежей
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS payments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    invoice_id TEXT UNIQUE,
                    amount REAL,
                    status TEXT DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            """)
            
            conn.commit()
            conn.close()
            logger.info("✅ База данных инициализирована")
        except Exception as e:
            logger.error(f"❌ Ошибка инициализации БД: {e}")
            raise
    
    def add_user(self, user_id: int, username: Optional[str] = None) -> bool:
        """Добавить пользователя."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR IGNORE INTO users (user_id, username)
                VALUES (?, ?)
            """, (user_id, username))
            
            conn.commit()
            conn.close()
            logger.info(f"✅ Пользователь {user_id} добавлен")
            return True
        except Exception as e:
            logger.error(f"❌ Ошибка добавления пользователя: {e}")
            return False
    
    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Получить пользователя."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return dict(row)
            return None
        except Exception as e:
            logger.error(f"❌ Ошибка получения пользователя: {e}")
            return None
    
    def is_vip(self, user_id: int) -> bool:
        """Проверить VIP статус."""
        try:
            user = self.get_user(user_id)
            if not user:
                return False
            
            is_vip = user.get("is_vip", 0)
            vip_expires = user.get("vip_expires_at")
            
            if not is_vip:
                return False
            
            if vip_expires:
                from datetime import datetime
                expires_dt = datetime.fromisoformat(vip_expires)
                if datetime.now() > expires_dt:
                    self.set_vip(user_id, False)
                    return False
            
            return True
        except Exception as e:
            logger.error(f"❌ Ошибка проверки VIP: {e}")
            return False
    
    def set_vip(self, user_id: int, is_vip: bool, expires_at: Optional[str] = None) -> bool:
        """Установить VIP статус."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE users 
                SET is_vip = ?, vip_expires_at = ?, updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
            """, (1 if is_vip else 0, expires_at, user_id))
            
            conn.commit()
            conn.close()
            logger.info(f"✅ VIP статус пользователя {user_id} обновлен: {is_vip}")
            return True
        except Exception as e:
            logger.error(f"❌ Ошибка установки VIP: {e}")
            return False
    
    def log_event(self, user_id: int, event_type: str, data: Optional[str] = None) -> bool:
        """Логировать событие."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO events (user_id, event_type, data)
                VALUES (?, ?, ?)
            """, (user_id, event_type, data))
            
            conn.commit()
            conn.close()
            logger.info(f"📝 Событие {event_type} для пользователя {user_id}")
            return True
        except Exception as e:
            logger.error(f"❌ Ошибка логирования события: {e}")
            return False
    
    def get_user_events(self, user_id: int, limit: int = 100) -> List[Dict[str, Any]]:
        """Получить события пользователя."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM events 
                WHERE user_id = ? 
                ORDER BY created_at DESC 
                LIMIT ?
            """, (user_id, limit))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"❌ Ошибка получения событий: {e}")
            return []
    
    def add_payment(self, user_id: int, invoice_id: str, amount: float) -> bool:
        """Добавить платеж."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO payments (user_id, invoice_id, amount)
                VALUES (?, ?, ?)
            """, (user_id, invoice_id, amount))
            
            conn.commit()
            conn.close()
            logger.info(f"💳 Платеж {invoice_id} добавлен для пользователя {user_id}")
            return True
        except Exception as e:
            logger.error(f"❌ Ошибка добавления платежа: {e}")
            return False
    
    def update_payment_status(self, invoice_id: str, status: str) -> bool:
        """Обновить статус платежа."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE payments 
                SET status = ?, updated_at = CURRENT_TIMESTAMP
                WHERE invoice_id = ?
            """, (status, invoice_id))
            
            conn.commit()
            conn.close()
            logger.info(f"💳 Статус платежа {invoice_id} обновлен: {status}")
            return True
        except Exception as e:
            logger.error(f"❌ Ошибка обновления платежа: {e}")
            return False
    
    def get_payment_by_invoice(self, invoice_id: str) -> Optional[Dict[str, Any]]:
        """Получить платеж по ID счета."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM payments WHERE invoice_id = ?", (invoice_id,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return dict(row)
            return None
        except Exception as e:
            logger.error(f"❌ Ошибка получения платежа: {e}")
            return None
