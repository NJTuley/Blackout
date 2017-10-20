import pygame
import Colors
import Fonts

class EpilepsyWarning():


    def __init__(self, screen):
        self.text_lines = [  # the lines of text to display in the waring
            'A very small percentage of people may experience a seizure when exposed',
            'to certain visual images, including flashing lights or patterns that may',
            'appear in video games. Even people who have no history of seizures or epilepsy',
            'may have an undiagnosed condition that can cause these “photosensitive epileptic',
            'seizures” while watching video games.',
            '',
            'These seizures may have a variety of symptoms, including lightheadedness, altered',
            'vision, eye or face twitching, jerking or shaking of arms or legs, disorientation,',
            'confusion, or momentary loss of awareness. Seizures may also cause loss of consciousness',
            'or convulsions that can lead to injury from falling down or striking nearby objects.',
            '',
            'Immediately stop playing and consult a doctor if you experience any of these symptoms.',
            'Parents should watch for or ask their children about the above symptoms. Children and ',
            'teenagers are more likely than adults to experience these seizures.',
            '',
            'The risk of photosensitive epileptic seizures may be reduced by taking the following precautions:',
            '',
            'Play in a well-lit room',
            'Do not play if you are drowsy or fatigued',
            'If you or any of your relatives have a history of seizures or epilepsy, consult a doctor before playing.'
        ]

        self.width = screen[0]
        self.height = screen[1]
        self.header = 'Photosensitive seizure warning'
        self.header = Fonts.medLarge.render(self.header, False,Colors.white)
        self.text_lines_rendered = []
        for i in range(len(self.text_lines)):
            self.text_lines_rendered.append(Fonts.small.render(self.text_lines[i], False, Colors.white))

    def run(self, gamewindow, fps, clock):
        self.counter = 0
        gamewindow.fill(Colors.black)
        while self.counter < fps * 15: # display warning for 10 seconds1
            gamewindow.blit(self.header, (self.width * 0.5 - self.header.get_width() * 0.5, self.height * 0.2- self.header.get_height() * 0.5))
            for i in range(len(self.text_lines_rendered)):
                gamewindow.blit(self.text_lines_rendered[i], (self.width * 0.5 - self.text_lines_rendered[i].get_width() * 0.5, self.height * 0.3 + (self.text_lines_rendered[i].get_height() * i)))
            self.counter += 1

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    return
                if event.type == pygame.QUIT:
                    pygame.quit()
            clock.tick(fps)
            pygame.display.update()