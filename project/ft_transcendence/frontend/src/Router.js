export class Router {
    constructor(routes) {
        this.routes = routes;
        this.init();
    }

    init() {
        window.addEventListener('popstate', () => this.handleRoute());
        this.handleRoute();
        this.addLinkListeners();
    }

    navigate(path) {
        history.pushState({}, path, path);
        this.handleRoute();
    }

    handleRoute() {
        const path = window.location.pathname;
        const route = this.routes[path] || this.routes['/404'];
        route.component.mount(document.getElementById('app'));
    }

    addLinkListeners() {
        document.body.addEventListener('click', (e) => {
            if (e.target.matches('a[data-link]')) {
                e.preventDefault();
                this.navigate(e.target.href);
            }
        });
    }
}