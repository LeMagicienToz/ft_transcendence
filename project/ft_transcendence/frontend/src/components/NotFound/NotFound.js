import { Component } from "../Component";

export class NotFound extends Component {
    render() {
        return `
            <section class="p-3">
                <h2>404 - Page Not Found</h2>
                <p>Sorry, the page you are looking for does not exist.</p>
            </section>
        `;
    }

    init() {
        console.log('NotFound component initialized');
    }
}