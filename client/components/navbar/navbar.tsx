import { Nav, Navbar, Badge, Container } from 'react-bootstrap';
import { useRouter } from "next/router";

export default function MyNavbar() {

    const router = useRouter()
    const currentPath = router.pathname;

    return (
        <>
            <Navbar collapseOnSelect expand="lg" bg="dark" variant="dark" className="color-nav">
                <Container>
                    <Navbar.Brand href="/">LinkDotCzech</Navbar.Brand>
                    <Navbar.Toggle aria-controls="responsive-navbar-nav" />
                    <Navbar.Collapse id="responsive-navbar-nav">
                        <Nav className="me-auto">
                            <Nav.Link href="/" active={currentPath === "/"}>Home</Nav.Link>
                            <Nav.Link href="/videos" active={currentPath === "/videos"}>Videos</Nav.Link>
                            {/* <Nav.Link href="/about">About</Nav.Link> */}
                        </Nav>
                    </Navbar.Collapse>
                </Container>
            </Navbar>
        </>
    )
}