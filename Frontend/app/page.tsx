'use client';
/*eslint-disable*/
import { Button, Flex, Img, Input, useColorModeValue } from '@chakra-ui/react';
import { useState } from 'react';
import Bg from '../public/img/chat/bg-image.png';
import Messages from '@/components/messages/Messages';
import FileInputModal from '@/components/fileInput/FileInputModal';
import axios from 'axios';
import { useParams } from 'next/navigation';

export default function Chat({
	messages = [],
}: {
	messages: { content: string; role: string }[];
}) {

	const { id: pdf_id } = useParams();
	// Input States
	const [local_messages, setLocalMessages] =
		useState<{ content: string; role: string }[]>(messages || []);

	const [inputCode, setInputCode] = useState<string>('');

	// Loading state
	const [loading, setLoading] = useState<boolean>(false);

	// API Key
	// const [apiKey, setApiKey] = useState<string>(apiKeyApp);
	const borderColor = useColorModeValue('gray.200', 'whiteAlpha.200');
	const inputColor = useColorModeValue('navy.700', 'white');
	const placeholderColor = useColorModeValue(
		{ color: 'gray.500' },
		{ color: 'whiteAlpha.600' },
	);

	const handleTranslate = async (e: any) => {
		e.preventDefault()
		if (!inputCode || !pdf_id) {
			alert('Please enter your message.');
			return;
		}
		setLocalMessages((lm) => [
			...lm,
			{ content: inputCode, role: 'user' },
		]);
		setLoading(true);
		setInputCode("");

		let target = document.querySelector("#messages_parent")
		target?.scroll({ top: target.scrollHeight, behavior: 'smooth' })

		try {
			const response = await axios.post(
				process.env.NEXT_PUBLIC_API_URL + '/get_reply',
				{
					text_input: inputCode,
					pdf_id: pdf_id,
				},
			);
			const answer = response.data.data.answer;

			setLocalMessages((lm) => [
				...lm,
				{ content: answer, role: 'model' },
			]);
			target = document.querySelector("#messages_parent")
			target?.scroll({ top: target.scrollHeight, behavior: 'smooth' })
		} catch (error) {
			console.error('Error getting messages', error);
		}
		setLoading(false);
	};

	const handleChange = (Event: any) => {
		setInputCode(Event.target.value);
	};

	return (
		<Flex
			w="100%"
			pt={{ base: '20px', md: '0px' }}
			direction="column"
			position="relative"
		>
			<FileInputModal />
			<Img
				src={Bg.src}
				position={'absolute'}
				w="350px"
				left="50%"
				top="50%"
				transform={'translate(-50%, -50%)'}
			/>
			<Flex
				direction="column"
				mx="auto"
				w={{ base: '100%', md: '100%', xl: '100%' }}
				minH={{ base: '75vh', '2xl': '85vh' }}
				maxW="1000px"
			>
				{/* Model Change */}
				<Flex direction={'column'} w="100%" maxH={{ base: '65vh', '2xl': '75vh' }} overflow="auto" id="messages_parent"
					mb={'auto'}>
					<Messages messages={local_messages} />
				</Flex>
				{/* Main Box */}

				{/* Chat Input */}
				<form onSubmit={handleTranslate}>
					<Flex
						ms={{ base: '0px', xl: '60px' }}
						mt="20px"
						justifySelf={'flex-end'}
					>
						<Input
							minH="54px"
							h="100%"
							border="1px solid"
							borderColor={borderColor}
							borderRadius="45px"
							p="15px 20px"
							me="10px"
							fontSize="sm"
							fontWeight="500"
							_focus={{ borderColor: 'none' }}
							color={inputColor}
							_placeholder={placeholderColor}
							placeholder="Type your message here..."
							onChange={handleChange}
							value={inputCode}
						/>
						<Button
							variant="primary"
							py="20px"
							px="16px"
							fontSize="sm"
							borderRadius="45px"
							ms="auto"
							w={{ base: '160px', md: '210px' }}
							h="54px"
							_hover={{
								boxShadow:
									'0px 21px 27px -10px rgba(96, 60, 255, 0.48) !important',
								bg: 'linear-gradient(15.46deg, #4A25E1 26.3%, #7B5AFF 86.4%) !important',
								_disabled: {
									bg: 'linear-gradient(15.46deg, #4A25E1 26.3%, #7B5AFF 86.4%)',
								},
							}}
							type='submit'
							isLoading={loading}
						>
							Submit
						</Button>
					</Flex>
				</form>
			</Flex>
		</Flex>
	);
}
