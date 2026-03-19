export const API_URL = 'http://localhost:8000'
export const WS_URL = 'ws://localhost:8000'

export const LANGUAGES = [
  { value: 'en', title: 'English' },
  { value: 'ru', title: 'Русский' },
  { value: 'be', title: 'Беларуская' },
  { value: 'uk', title: 'Українська' }
]

export const CURRENCIES = [
  { value: 'USD', symbol: '$' },
  { value: 'EUR', symbol: '€' },
  { value: 'RUB', symbol: '₽' },
  { value: 'BYN', symbol: 'Br' },
  { value: 'UAH', symbol: '₴' }
]

export const userType = {
  ADMIN: 1,
  CUSTOMER: 2,
  ORGANIZER: 3
}

export const chatType = {
  DIALOG: 1,
  GROUP: 2
}

export const messageType = {
  TEXT: 1,
  IMAGES: 2,
  FILES: 3
}

export const reasonOfNotification = {
  FOLLOW: 1,
  ARTICLE: 2,
  ALBUM: 3,
  PHOTO: 4,
  LIKE_ALBUM: 5,
  LIKE_PHOTO: 6,
  COMMENT: 7,
  REVIEW: 8,
  MESSAGE: 9
}
