const routes = [
  {
    path: '/admin',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      { path: 'dashboard', component: () => import('pages/Index.vue') },

      { path: 'categories', component: () => import('pages/admin/Categories/Index') },
      { path: 'articles', component: () => import('pages/admin/Articles/Index') },
      { path: 'users', component: () => import('pages/admin/Users/Index') },
      { path: 'block_users', component: () => import('pages/admin/BlockUsers/Index') },
      { path: 'products', component: () => import('pages/admin/Products/Index') },
      { path: 'colors', component: () => import('pages/admin/Colors/Index') },
      { path: 'sizes', component: () => import('pages/admin/Sizes/Index') },
      { path: 'suggests', component: () => import('pages/admin/Suggests/Index') },
      { path: 'images', component: () => import('pages/admin/Images/Index') },
      { path: 'carts', component: () => import('pages/admin/Carts/Index') },
      { path: 'coupons', component: () => import('pages/admin/Coupons/Index') },
      { path: 'payments', component: () => import('pages/admin/Payments/Index') },
      { path: 'comments', component: () => import('pages/admin/Comments/Index') },
      { path: 'likes_dislikes', component: () => import('pages/admin/Likes_And_DisLikes/Index') },
      { path: 'wishlists', component: () => import('pages/admin/WishLists/Index') },
      { path: 'sliders', component: () => import('pages/admin/Sliders/Index') },
      { path: 'settings', component: () => import('pages/admin/Settings/Index') },
      { path: 'newsletters', component: () => import('pages/admin/Newsletter/Index') },
      { path: 'stars', component: () => import('pages/admin/Stars/Index') },
      { path: 'notify_users', component: () => import('pages/admin/NotifyUsers/Index') },
      { path: 'orders', component: () => import('pages/admin/Orders/Index') },
      { path: 'contact_us', component: () => import('pages/admin/Contact_us/Index') }

    ]
  },

  {
    path: '/admin/tickets',
    component:
      () => import('layouts/MainLayout.vue'),
    children:
      [
        { path: '', component: () => import('pages/admin/Tickets/Tickets/Index') },
        { path: 'questions', component: () => import('pages/admin/Tickets/Questions/Index') },
        { path: 'answers', component: () => import('pages/admin/Tickets/Answers/Index') }
      ]
  },

  {
    path: '/admin/ACL',
    component:
      () => import('layouts/MainLayout.vue'),
    children:
      [
        { path: 'roles', component: () => import('pages/admin/ACL/Roles/Index') },
        { path: 'permissions', component: () => import('pages/admin/ACL/Permissions/Index') },
        { path: 'role_user', component: () => import('pages/admin/ACL/Role_User/Index') },
        { path: 'role_permission', component: () => import('pages/admin/ACL/Role_Permission/Index') }
      ]
  },

  //    ###  User Panel ###
  {
    path: '/panel',
    component:
      () => import('layouts/MainLayout.vue'),
    children:
      [
        { path: 'dashboard', component: () => import('pages/Index.vue') },
        { path: 'profile', component: () => import('pages/Profile') },
        { path: 'orders', component: () => import('pages/panel/Orders/Index') }
      ]
  },
  //    ###  Authentication ###

  {
    path: '/login',
    component:
      () => import('pages/Auth/login')
  },

  {
    path: '/register',
    component:
      () => import('pages/Auth/register')
  },

  {
    path: '/password/reset',
    component:
      () => import('pages/Auth/reset_password')
  },

  {
    path: '/password/reset/confirm',
    component:
      () => import('pages/Auth/reset_password_confirm')
  },

  {
    path: '/email/verify',
    component:
      () => import('pages/Auth/verify_email')
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '*',
    component:
      () => import('pages/Error404.vue')
  }
]

export default routes
