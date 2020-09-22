trainingData = {
	# "IDs": [ "H2017_Mg0","H2017_Mg3","H2017_Mg6","H2017_Mg12","H2017_Mg60"],
	"IDs": [ "H2017_Mg0","H2017_Mg3","H2017_Mg6","H2017_Mg12","H2017_Mg60","B2016_C","B2016_M"],
	#"IDs": ["H2017_Mg0"],
	#"IDs": [ "B2016_C","B2016_M"],
	"scale": 0.025,
	"H2017_Mg0": {
		"setup": {
			"exp_duration": 72,
			"grid": {
				"area": 1,
				"volume": 0.274,
				"patch_size": 0.012774976
			},
			"patch": {
				"attrs": {
					"Mg": 0,
					"pH": 7.8
				}
			},
			"agents": {
				"n": {
					"MSC": 2739,
					"Dead": 0
				},
				"MSC": {
					"attrs": {
						"pH": 7.8
					}
				},
				"Dead": {
					"attrs": {}
				}
			}
		},

		"expectations": {
			"timepoints": [ "24", "48", "72" ],
			"24": {
				"liveCellCount": 3287,
				"viability": 71
			},
			"48": {
				"liveCellCount": 7123,
				"viability": 73
			},
			"72": {
				"liveCellCount": 10136,
				"viability": 60
			}
		}
	},
	"H2017_Mg3": {
		"setup": {
			"exp_duration": 72,
			"grid": {
				"area": 1,
				"volume": 0.274,
				"patch_size": 0.012774976

			},
			"patch": {
				"attrs": {
					"Mg": 3.6,
					"pH": 7.8
				}
			},
			"agents": {
				"n": {
					"MSC": 2739,
					"Dead": 0
				},
				"MSC": {
					"attrs": {
						"pH": 7.8
					}
				},
				"Dead": {
					"attrs": {}
				}
			}
		},
		"expectations": {
			"timepoints": [ "24", "48", "72" ],
			"24": {
				"liveCellCount": 3424,
				"viability": 68
			},
			"48": {
				"liveCellCount": 6575,
				"viability": 80
			},
			"72": {
				"liveCellCount": 13150,
				"viability": 51
			}
		}
	},
	"H2017_Mg6": {
		"setup": {
			"exp_duration": 72,
			"grid": {
				"area": 1,
				"volume": 0.274,
				"patch_size": 0.012774976

			},
			"patch": {
				"attrs": {
					"Mg": 6,
					"pH": 7.8
				}
			},
			"agents": {
				"n": {
					"MSC": 2739,
					"Dead": 0
				},
				"MSC": {
					"attrs": {
						"pH": 7.8
					}
				},
				"Dead": {
					"attrs": {}
				}
			}
		},
		"expectations": {
			"timepoints": [ "24", "48", "72" ],
			"24": {
				"liveCellCount": 3013,
				"viability": 69
			},
			"48": {
				"liveCellCount": 6301,
				"viability": 81
			},
			"72": {
				"liveCellCount": 9863,
				"viability": 52
			}
		}
	},
	"H2017_Mg12": {
		"setup": {
			"exp_duration": 72,
			"grid": {
				"area": 1,
				"volume": 0.274,
				"patch_size": 0.012774976

			},
			"patch": {
				"attrs": {
					"Mg": 12,
					"pH": 7.8
				}
			},
			"agents": {
				"n": {
					"MSC": 2739,
					"Dead": 0
				},
				"MSC": {
					"attrs": {
						"pH": 7.8
					}
				},
				"Dead": {
					"attrs": {}
				}
			}
		},
		"expectations": {
			"timepoints": [ "24", "48", "72" ],
			"24": {
				"liveCellCount": 2191,
				"viability": 70
			},
			"48": {
				"liveCellCount": 4931,
				"viability": 61
			},
			"72": {
				"liveCellCount": 7123,
				"viability": 50
			}
		}
	},
	"H2017_Mg60": {
		"setup": {
			"exp_duration": 72,
			"grid": {
				"area": 1,
				"volume": 0.274,
				"patch_size": 0.012774976

			},
			"patch": {
				"attrs": {
					"Mg": 60,
					"pH": 7.8
				}
			},
			"agents": {
				"n": {
					"MSC": 2739,
					"Dead": 0
				},
				"MSC": {
					"attrs": {
						"pH": 7.8
					}
				},
				"Dead": {
					"attrs": {}
				}
			}
		},
		"expectations": {
			"timepoints": [ "24", "48", "72" ],
			"24": {
				"liveCellCount": 1643,
				"viability": 55
			},
			"48": {
				"liveCellCount": 2191,
				"viability": 60
			},
			"72": {
				"liveCellCount": 2191,
				"viability": 51
			}
		}
	},
	"B2016_C": {
		"setup": {
			"exp_duration": 504,
			"grid": {
				"area": 1,
				"volume": 0.313,
				"patch_size": 0.013
			},
			"patch": {
				"attrs": {
					"Mg": 0,
					"pH": 7.8
				}
			},
			"agents": {
				"n": {
					"MSC": 5208,
					"Dead": 0
				},
				"MSC": {
					"attrs": {
						"pH": 7.8
					}
				},
				"Dead": {
					"attrs": {}
				}
			}
		},
		"expectations": {
			"timepoints": [ "168", "336", "504" ],
			"168": {
				"DNA":26.95,
				"viability": "70  80",
				"OC": 0.53,
				"ALP": 0.30,
				"nTGF": 1.24,
				"nBMP":0.13
			},
			"336": {
				"DNA":18.53,
				"viability": "70  80",
				"OC": 0.71,
				"ALP": 0.53,
				"nTGF": 1.87,
				"nBMP":1.4
			},
			"504": {
				"DNA":20.73,
				"viability": "70  80",
				"OC": 0.8,
				"ALP": 0.57,
				"nTGF": 1.21,
				"nBMP":0.37
			}
		}
	},
	"B2016_M": {
		"setup": {
			"exp_duration": 504,
			"grid": {
				"area": 1,
				"volume": 0.313,
				"patch_size": 0.013
			},
			"patch": {
				"attrs": {
					"Mg": 5,
					"pH": 7.8
				}
			},
			"agents": {
				"n": {
					"MSC": 5208,
					"Dead": 0
				},
				"MSC": {
					"attrs": {
						"pH": 7.8
					}
				},
				"Dead": {
					"attrs": {}
				}
			}
		},
		"expectations": {
			"timepoints": [ "168", "336", "504" ],
			"168": {
				"DNA":27.65,
				"viability": "70  80",
				"OC": 0.28,
				"ALP": 0.34,
				"nTGF": 1.1,
				"nBMP":0.14
			},
			"336": {
				"DNA":25.02,
				"viability": "70  80",
				"OC": 0.22,
				"ALP": 0.39,
				"nTGF": 0.97,
				"nBMP":0.56
			},
			"504": {
				"DNA":19.71,
				"viability": "70  80",
				"OC": 0.27,
				"ALP": 0.61,
				"nTGF": 1.21,
				"nBMP":0.37
			}
		}
	}





}
