'use client';
// chakra imports
import { Flex, Button, Icon } from '@chakra-ui/react';
import Brand from '@/components/sidebar/components/Brand';
import { MdOutlineFileUpload } from 'react-icons/md';
import Link from 'next/link';

// FUNCTIONS

function SidebarContent() {
	// SIDEBAR
	return (
		<Flex
			direction="column"
			height="100%"
			pt="20px"
			pb="26px"
			borderRadius="30px"
			maxW="285px"
			px="20px"
		>
			<Brand />
			<Link href="/" style={{maxWidth:"fit-content", margin:"0 auto"}}>
				<Button
					variant="primary"
					py="20px"
					px="16px"
					fontSize="sm"
					borderRadius="45px"
					mx="auto"
					w={{ base: '160px', md: '210px' }}
					h="54px"
					_hover={{
						boxShadow: '0px 21px 27px -10px rgba(96, 60, 255, 0.48) !important',
						bg: 'linear-gradient(15.46deg, #4A25E1 26.3%, #7B5AFF 86.4%) !important',
						_disabled: {
							bg: 'linear-gradient(15.46deg, #4A25E1 26.3%, #7B5AFF 86.4%)',
						},
					}}
					type="button"
				>
					<Icon as={MdOutlineFileUpload} width="20px" height="20px" />
					Upload new PDF
				</Button>
			</Link>
		</Flex>
	);
}

export default SidebarContent;
