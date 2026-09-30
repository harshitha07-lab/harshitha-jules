from main import main


def test_main(capsys) -> None:
    main()
    captured = capsys.readouterr()
    assert captured.out == "Hello, World!\n"
