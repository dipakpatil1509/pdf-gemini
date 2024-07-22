'use client';
import React, { ReactNode } from 'react';
import { Box} from '@chakra-ui/react';
import routes from '@/routes';
import Sidebar from '@/components/sidebar/Sidebar';
import '@/styles/App.css';
import '@/styles/Contact.css';
import '@/styles/Plugins.css';
import '@/styles/MiniCalendar.css';
import AppWrappers from './AppWrappers';

export default function RootLayout({ children }: { children: ReactNode }) {
	return (
		<html lang="en">
			<title>PDF Gemini</title>
			<body id={'root'}>
				<AppWrappers>
					<Box>
						<Sidebar routes={routes} />
						<Box
							pt={{ base: '0px', md: '0px' }}
							float="right"
							minHeight="100vh"
							height="100%"
							overflow="auto"
							position="relative"
							maxHeight="100%"
							w={{ base: '100%', xl: 'calc( 100% - 290px )' }}
							maxWidth={{ base: '100%', xl: 'calc( 100% - 290px )' }}
							transition="all 0.33s cubic-bezier(0.685, 0.0473, 0.346, 1)"
							transitionDuration=".2s, .2s, .35s"
							transitionProperty="top, bottom, width"
							transitionTimingFunction="linear, linear, ease"
						>
							<Box
								mx="auto"
								p={{ base: '20px', md: '30px' }}
								pe="20px"
								minH="100vh"
								pt="20px"
							>
								{children}
							</Box>
						</Box>
					</Box>
				</AppWrappers>
			</body>
		</html>
	);
}
