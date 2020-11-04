trainingData = {
	#"IDs": [ "H2017_Mg0","H2017_Mg3","H2017_Mg6","H2017_Mg12","H2017_Mg60"],
	# "IDs": [ "H2017_Mg0","H2017_Mg3","H2017_Mg6","H2017_Mg12","H2017_Mg60","B2016_C","B2016_M"],
	# "IDs": ["B2016_M"],
	"IDs": [ "B2016_C","B2016_M"],
	#"IDs": [ "X_1_C","X_1_M3","X_1_M7","X_1_M14"],
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
					"Mg": 0.74,
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
				"DNA":8.421277778,
				"OC": 0.53,
				"ALP": 0.30,
				"nTGF": 1.24,
				"nBMP":0.13,
				'viability': '50 100'
			},
			"336": {
				"DNA":5.79028125,
				"OC": 0.71,
				"ALP": 0.53,
				"nTGF": 1.87,
				"nBMP":1.4,
				'viability': '50 100'
			},
			"504": {
				"DNA":6.478159722,
				"OC": 0.8,
				"ALP": 0.57,
				"nTGF": 1.21,
				"nBMP":0.37,
				'viability': '50 100'
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
			"DNA":8.640232639,
				"OC": 0.28,
				"ALP": 0.34,
				"nTGF": 1.1,
				"nBMP":0.14,
				'viability': '50 100'
			},
			"336": {
				"DNA":7.818329861,
				"OC": 0.22,
				"ALP": 0.39,
				"nTGF": 0.97,
				"nBMP":0.56,
				'viability': '50 100'
			},
			"504": {
				"DNA":6.160513889,
				"OC": 0.27,
				"ALP": 0.61,
				"nTGF": 1.21,
				"nBMP":0.37,
				'viability': '50 100'
			}
		}
	},
	"X_1_C": {
		"setup": {
			"exp_duration": 216,
			"grid": {
				"area": 1,
				"volume": 0.313,
				"patch_size": 0.013
			},
			"patch": {
				"attrs": {
					"Mg": .7,
					"pH": 7.8
				}
			},
			"agents": {
				"n": {
					"MSC": 2631,
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
			"timepoints": [ "72", "144", "216" ],
			"72": {
				"liveCellCount":19219
			},
			"144": {
				"liveCellCount":32401
			},
			"216": {
				"liveCellCount":65710
			}
		}
	},
	"X_1_M3": {
		"setup": {
			"exp_duration": 216,
			"grid": {
				"area": 1,
				"volume": 0.313,
				"patch_size": 0.013
			},
			"patch": {
				"attrs": {
					"Mg": .7,
					"pH": 7.8
				}
			},
			"agents": {
				"n": {
					"MSC": 2631,
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
			"timepoints": [ "72", "144", "216" ],
			"72": {
				"liveCellCount":16602
			},
			"144": {
				"liveCellCount":46754
			},
			"216": {
				"liveCellCount":106053
			}
		}
	},
	"X_1_M7": {
		"setup": {
			"exp_duration": 216,
			"grid": {
				"area": 1,
				"volume": 0.313,
				"patch_size": 0.013
			},
			"patch": {
				"attrs": {
					"Mg": .7,
					"pH": 7.8
				}
			},
			"agents": {
				"n": {
					"MSC": 2631,
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
			"timepoints": [ "72", "144", "216" ],
			"72": {
				"liveCellCount":13765
			},
			"144": {
				"liveCellCount":49915
			},
			"216": {
				"liveCellCount":86163
			}
		}
	},
	"X_1_M14": {
		"setup": {
			"exp_duration": 216,
			"grid": {
				"area": 1,
				"volume": 0.313,
				"patch_size": 0.013
			},
			"patch": {
				"attrs": {
					"Mg": .7,
					"pH": 7.8
				}
			},
			"agents": {
				"n": {
					"MSC": 2631,
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
			"timepoints": [ "72", "144", "216" ],
			"72": {
				"liveCellCount":8277
			},
			"144": {
				"liveCellCount":26134
			},
			"216": {
				"liveCellCount":46675
			}
		}
	}





}
