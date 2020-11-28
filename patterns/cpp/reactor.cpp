#include <iostream>
#include <fstream>
#include <map>
#include <chrono>
#include <thread>

enum Event_Type {
    INPUT_EVENT = 01,
    FILE_INPUT_EVENT = 02,

};

class EventHandler;

class Reactor {
public:

    static Reactor* getInstance();
    int register_handler(EventHandler *eh, Event_Type et);
    int remove_handler(EventHandler &eh, Event_Type et);
    void handle_events(int time_out = 0);

protected:

    Reactor() = default;

private:

    std::map<int, EventHandler*> inputHandles;
    std::map<int, EventHandler*> fileInputHandles;
    bool stop_param = false;
    static Reactor *instance;

};

class EventHandler {
public:

    explicit EventHandler(int new_id) : id(new_id){};
    int get_handler_id() const { return id; }
    virtual bool handle_input(){ return true; };
    virtual bool handle_file_input(){ return true; };
    
private:

    int id;

};

class InputHandler : public EventHandler {
public:

    InputHandler(int new_id, std::string destination_file) : EventHandler(new_id),
                    destination(std::move(destination_file)){};

    bool handle_input() override {
        try {
            std::ofstream out_file;
            out_file.open(destination);
            std::string input;
            std::cout << "Input kann getätigt werden:" << std::endl;
            while (std::getline(std::cin, input) && !input.empty()) {
                out_file << input.c_str() << std::endl;
            }
            out_file.close();
        } catch (std::exception &ex) {
            std::cout << ex.what() << std::endl;
            Reactor::getInstance()->remove_handler(dynamic_cast<EventHandler &>(*this), Event_Type::INPUT_EVENT);
            return false;
        }
        Reactor::getInstance()->remove_handler(dynamic_cast<EventHandler &>(*this), Event_Type::INPUT_EVENT);
        return true;
    }

private:

    std::string destination;

};

class FileInputHandler : public EventHandler {
public:

    FileInputHandler(int new_id, std::string source_file, std::string destination_file)
    : EventHandler(new_id), source(std::move(source_file)), destination(std::move(destination_file)){};

    bool handle_file_input() override {
        try {
            std::string input;
            std::ifstream source_file(source);
            std::ofstream out_file(destination);
            out_file << "//copied file" << std::endl;
            while (std::getline(source_file, input) && !input.empty()) {
                out_file << input.c_str() << std::endl;
            }
            out_file.close();
            source_file.close();
        } catch (std::exception &ex) {
            std::cout << ex.what() << std::endl;
            Reactor::getInstance()->remove_handler(dynamic_cast<EventHandler &>(*this), Event_Type::FILE_INPUT_EVENT);
            return false;
        }
        Reactor::getInstance()->remove_handler(dynamic_cast<EventHandler &>(*this), Event_Type::FILE_INPUT_EVENT);
        return true;
    }

private:
    std::string source;
    std::string destination;
};



int Reactor::register_handler(EventHandler *eh, Event_Type et){
    if (et == INPUT_EVENT) {
        inputHandles.insert(std::pair<int, EventHandler*>(eh->get_handler_id(), eh));
    } else if (et == FILE_INPUT_EVENT) {
        fileInputHandles.insert(std::pair<int, EventHandler*>(eh->get_handler_id(), eh));
    } else {
        // reserved for future handlers
    }
    return 0;
}

int Reactor::remove_handler(EventHandler &eh, Event_Type et) {
    if (et == INPUT_EVENT) {
        inputHandles.erase(eh.get_handler_id());
    } else if (et == FILE_INPUT_EVENT) {
        fileInputHandles.erase(eh.get_handler_id());
    } else {
        // reserved for future handlers
    }
    return 0;
}

void Reactor::handle_events(int time_out) {

    while (!stop_param) {

        // time out
        std::this_thread::sleep_for(std::chrono::seconds(time_out));

        for (auto map_entry : inputHandles) {
            if (map_entry.second->handle_input())
                std::cout << "input event " << map_entry.first << " successfully handled!" << std::endl;
            else
                std::cout << "input event " << map_entry.first << " errored out!" << std::endl;
            if (inputHandles.empty())
                break;
        }

        for (auto map_entry : fileInputHandles) {
            if (map_entry.second->handle_file_input())
                std::cout << "file_input event " << map_entry.first << " successfully handled!" << std::endl;
            else
                std::cout << "file_input event " << map_entry.first << " errored out!" << std::endl;
            if (fileInputHandles.empty())
                break;
        }

        // stop if no events given
        if (inputHandles.empty() && fileInputHandles.empty()) {
            stop_param = true;
        }
    }

}

Reactor* Reactor::instance = nullptr;

Reactor* Reactor::getInstance() {
    if (instance == nullptr)
        instance = new Reactor();
    return instance;
}

int main() {

    Reactor *example_reactor = Reactor::getInstance();
    example_reactor->register_handler(new InputHandler(0, "input_handler_example_file.txt"),
            Event_Type::INPUT_EVENT);
    example_reactor->register_handler(new FileInputHandler(0,
            "example_params.txt", "file_input_handler_example_file.txt"),
            Event_Type::FILE_INPUT_EVENT);
    example_reactor->handle_events();


    return 0;
}
