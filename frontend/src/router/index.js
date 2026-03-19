import i18n, {
  SUPPORT_LOCALES,
  loadLocaleMessages,
  setI18nLanguage
} from '@/i18n'
import { createRouter, createWebHistory } from 'vue-router'
import Root from './Root.vue'

function isAuthenticated(to, from) {
  const isLoggedIn = window.localStorage.getItem('user')
  if (!isLoggedIn) {
    return {
      name: 'Login',
      params: { locale: i18n.global.locale.value },
      query: { redirect: to.fullPath }
    }
  }
}

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/:locale',
      name: 'Root',
      component: Root,
      children: [
        {
          path: '',
          name: 'Home',
          component: () => import('@/views/HomeView.vue')
        },
        {
          path: 'organizers',
          name: 'OrganizerList',
          component: () => import('@/views/organizers/ListView.vue')
        },
        {
          path: 'organizers/:profile_url',
          name: 'OrganizerDetail',
          component: () => import('@/views/organizers/DetailView.vue')
        },
        {
          path: 'albums',
          name: 'AlbumList',
          component: () => import('@/views/portfolio/AlbumListView.vue')
        },
        {
          path: 'albums/:uuid',
          name: 'AlbumDetail',
          component: () => import('@/views/portfolio/AlbumDetailView.vue')
        },
        {
          path: 'photos',
          name: 'PhotoList',
          component: () => import('@/views/portfolio/PhotoListView.vue')
        },
        {
          path: 'photos/:uuid',
          name: 'PhotoDetail',
          component: () => import('@/views/portfolio/PhotoDetailView.vue')
        },
        {
          path: 'blog',
          name: 'BaseBlog',
          component: () => import('@/views/blog/BaseBlogView.vue'),
          children: [
            {
              path: '',
              name: 'ArticleList',
              component: () => import('@/views/blog/ArticleListView.vue')
            },
            {
              path: ':slug',
              name: 'ArticleDetail',
              component: () => import('@/views/blog/ArticleDetailView.vue')
            }
          ]
        },
        {
          path: 'tags/:uuid',
          name: 'TagDetail',
          component: () => import('@/views/TagDetailView.vue')
        },
        {
          path: 'about',
          name: 'About',
          component: () => import('@/views/AboutView.vue')
        },
        {
          path: 'feedback',
          name: 'Feedback',
          component: () => import('@/views/FeedbackView.vue')
        },
        {
          path: '',
          name: 'BaseAuth',
          component: () => import('@/views/auth/BaseAuthView.vue'),
          beforeEnter: (to, from) => {
            const isLoggedIn = window.localStorage.getItem('user')
            if (isLoggedIn) {
              return {
                name: 'Profile',
                params: { locale: i18n.global.locale.value }
              }
            }
          },
          children: [
            {
              path: 'login',
              name: 'Login',
              component: () => import('@/views/auth/LoginView.vue')
            },
            {
              path: 'registration',
              name: 'Registration',
              component: () => import('@/views/auth/RegistrationView.vue')
            },
            {
              path: 'activation/:uid/:token',
              name: 'Activation',
              component: () => import('@/views/auth/ActivationView.vue')
            },
            {
              path: 'password/reset',
              name: 'PasswordReset',
              component: () => import('@/views/auth/PasswordResetView.vue')
            },
            {
              path: 'password/reset/:uid/:token',
              name: 'PasswordResetConfirm',
              component: () => import('@/views/auth/PasswordResetConfirmView.vue')
            }
          ]
        },
        {
          path: 'settings',
          name: 'BaseSettings',
          component: () => import('@/views/auth/BaseSettingsView.vue'),
          beforeEnter: [isAuthenticated],
          children: [
            {
              path: 'profile',
              name: 'Profile',
              component: () => import('@/views/auth/ProfileView.vue')
            },
            {
              path: 'profile/delete',
              name: 'ProfileDelete',
              component: () => import('@/views/auth/ProfileDeleteView.vue')
            },
            {
              path: 'password/change',
              name: 'PasswordChange',
              component: () => import('@/views/auth/PasswordChangeView.vue')
            },
            {
              path: 'social-links',
              name: 'SocialLinks',
              component: () => import('@/views/auth/SocialLinksView.vue')
            },
            {
              path: 'portfolio',
              name: 'Portfolio',
              component: () => import('@/views/auth/portfolio/PortfolioView.vue')
            },
            {
              path: 'portfolio/albums',
              name: 'PortfolioAlbumList',
              component: () => import('@/views/auth/portfolio/AlbumListView.vue')
            },
            {
              path: 'portfolio/albums/:uuid',
              name: 'PortfolioAlbumDetail',
              component: () => import('@/views/auth/portfolio/AlbumDetailView.vue')
            },
            {
              path: 'portfolio/photos',
              name: 'PortfolioPhotoList',
              component: () => import('@/views/auth/portfolio/PhotoListView.vue')
            }
          ]
        },
        {
          path: 'messenger',
          name: 'BaseMessenger',
          component: () => import('@/views/messenger/BaseMessengerView.vue'),
          beforeEnter: [isAuthenticated],
          children: [
            {
              path: '',
              name: 'Messenger',
              component: () => import('@/views/messenger/MessengerView.vue')
            },
            {
              path: ':uuid',
              name: 'Chat',
              component: () => import('@/views/messenger/ChatView.vue')
            }
          ]
        },
        {
          path: 'followers',
          name: 'Followers',
          component: () => import('@/views/FollowersView.vue'),
          beforeEnter: [isAuthenticated]
        },
        {
          path: 'following',
          name: 'Following',
          component: () => import('@/views/FollowingView.vue'),
          beforeEnter: [isAuthenticated]
        },
        {
          path: 'favorites',
          name: 'Favorites',
          component: () => import('@/views/FavoritesView.vue'),
          beforeEnter: [isAuthenticated]
        }
      ]
    },
    {
      path: '/:pathMatch(.*)*',
      name: 'NotFound',
      component: () => import('@/views/NotFoundView.vue')
    }
  ],
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

router.beforeEach(async (to, from) => {
  let paramsLocale = to.params.locale

  if (!paramsLocale) {
    const arg_from_path = to.path.split('/')[1]
    if (SUPPORT_LOCALES.includes(arg_from_path)) {
      paramsLocale = arg_from_path
    } else {
      return '/' + i18n.global.locale.value + to.path
    }
  } else if (!SUPPORT_LOCALES.includes(paramsLocale)) {
    return '/' + i18n.global.locale.value + to.path
  }

  if (!i18n.global.availableLocales.includes(paramsLocale)) {
    await loadLocaleMessages(i18n, paramsLocale)
  }

  if (paramsLocale !== i18n.global.locale.value) {
    setI18nLanguage(i18n, paramsLocale)
  }
})

export default router
