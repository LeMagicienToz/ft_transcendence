// import 'bootstrap/dist/css/bootstrap.min.css';
// import './main.scss';
// import { Header } from './components/Header/Header.js';
// import { Home } from './components/Home/Home.js';
// import { About } from './components/About/About.js';
// import { NotFound } from './components/NotFound/NotFound.js';
// import { Router } from './Router.js';
// import { Store } from './Store.js';

// document.addEventListener('DOMContentLoaded', () => {
//     const appStore = new Store({ count: 0, user: { name: 'John Doe' } });

//     const header = new Header({ title: 'My Vanilla JS SPA HEADER' });
//     header.mount(document.getElementById('header'));

//     const routes = {
//         '/': { component: new Home({ store: appStore }) },
//         '/about': { component: new About({ store: appStore }) },
//         '/404': { component: new NotFound() }
//     };

//     new Router(routes);
// });